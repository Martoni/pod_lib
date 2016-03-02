---------------------------------------------------------------------------
-- Company     : ARMadeus Systems
-- Author(s)   : Fabien Marteau
--
-- Creation Date : 05/03/2008
-- File          : led.vhd
--
-- Abstract : drive one led with Wishbone bus
--
---------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.all;

Entity led is
    generic(
        id : natural := 1;
        wb_size : natural := 16 -- Data port size for wishbone
    );
    port
    (
        -- Wishbone signals
        wbs_reset    : in std_logic;
        wbs_clk      : in std_logic;
        wbs_add       : in std_logic;
        wbs_writedata : in std_logic_vector( wb_size-1 downto 0);
        wbs_readdata  : out std_logic_vector( wb_size-1 downto 0);
        wbs_strobe    : in std_logic;
        wbs_cycle     : in std_logic;
        wbs_write     : in std_logic;
        wbs_ack       : out std_logic;
        -- out signals
        led : out std_logic
    );
end entity led;

Architecture led_1 of led is
    signal reg : std_logic_vector( wb_size-1 downto 0);
    signal readdata_s : std_logic_vector(wb_size-1 downto 0);
    signal read_ack, write_ack : std_logic;
begin

    -- connect led
    led <= reg(0);

    -- manage register
    write_bloc : process(wbs_clk, wbs_reset)
    begin
        if wbs_reset = '1' then
            write_ack <= '0';
            reg <= (others => '0');
        elsif rising_edge(wbs_clk) then
            reg <= reg;
            write_ack <= '0';
            if ((wbs_strobe and wbs_write and wbs_cycle) = '1' ) then
                write_ack <= '1';
                reg <= wbs_writedata;
            end if;
        end if;

    end process write_bloc;

    wbs_readdata <= readdata_s;
    read_bloc : process(wbs_clk, wbs_reset)
    begin
        if wbs_reset = '1' then
            readdata_s <= (others => '0');
        elsif rising_edge(wbs_clk) then
            readdata_s <= readdata_s;
            read_ack <= '0';
            if (wbs_strobe = '1' and wbs_write = '0'  and wbs_cycle = '1' ) then
                read_ack <= '1';
                if wbs_add = '0' then
                    readdata_s <= reg;
                else
                    readdata_s <= std_logic_vector(to_unsigned(id,wb_size));
                end if;
            end if;
        end if;
    end process read_bloc;

    wbs_ack <= read_ack or write_ack;

end architecture led_1;

