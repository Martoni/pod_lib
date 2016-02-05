-------------------------------------------------------------------------------
--
--  File          :  imx6_wb_wrapper.vhd
--  Related files :  (none)
--
--  Author(s)     :  Gwenhael Goavec-Merou <gwenhael.goavec-merou@trabucayre.com>
--  Project       :  i.MX6 wrapper to Wishbone bus
--
--  Creation Date :  20/07/2015
--
--  Description   :  This is the top file of the IP
-------------------------------------------------------------------------------
--  Modifications :
--
-------------------------------------------------------------------------------

library IEEE;
  use IEEE.std_logic_1164.all;
  use IEEE.numeric_std.all;

Entity imx6_wb_wrapper is
port
(
    refclk_clk : in std_logic;
    hip_serial_tx_out0 : out std_logic;
    hip_serial_rx_in0 : in std_logic;
    npor_pin_perst : in std_logic;
    npor_npor : in std_logic;
    -- candroutput
    clk_o : out std_logic;
    rst_o : out std_logic;
    -- irq
    irq_irq: in std_logic_vector(15 downto 0);
    -- Wishbone interface signals
    wbm_clk : out std_logic;
    wbm_rst : out std_logic;
    wbm_address    : out std_logic_vector(11 downto 0);  -- Address bus
    wbm_readdata   :  in std_logic_vector(63 downto 0);  -- Data bus for read access
    wbm_writedata  : out std_logic_vector(63 downto 0);  -- Data bus for write access
    wbm_byte_enable: out std_logic_vector(7 downto 0);
    wbm_strobe     : out std_logic;                      -- Data Strobe
    wbm_write      : out std_logic;                      -- Write access
    wbm_ack        :  in std_logic;                      -- acknowledge
    wbm_cycle      : out std_logic                       -- bus cycle in progress
);
end entity;

Architecture RTL of imx6_wb_wrapper is

    component imx6_wb_wrapper_qsys
        port (
            refclk_clk : in std_logic;
            hip_serial_tx_out0 : out std_logic;
            hip_serial_rx_in0 : in std_logic;
            npor_pin_perst : in std_logic;
            npor_npor : in std_logic;
            -- candroutput
            gls_rst_reset : out std_logic;
            gls_clk_clk : out std_logic;
            -- irq
            irq_irq: in std_logic_vector(15 downto 0);
            -- aval64
            aval_exp_address  : out std_logic_vector(11 downto 0);
            aval_exp_read : out std_logic;
            aval_exp_write : out std_logic;
            aval_exp_waitrequest : in std_logic;
            aval_exp_byteenable : out std_logic_vector(7 downto 0);
            aval_exp_readdatavalid : in std_logic;
            aval_exp_writedata : out std_logic_vector(63 downto 0);
            aval_exp_readdata : in std_logic_vector(63 downto 0)
    );
    end component;
    signal clk, reset : std_logic;
    signal aval_exp_read, aval_exp_write : std_logic;
    signal bus_enable : std_logic;
    signal wbm_readvalid_s : std_logic;
    signal waitrequest_next_s : std_logic;
begin

    wbm_clk <= clk;
    wbm_rst <= reset;
    clk_o <= clk;
    rst_o <= reset;


    imx6_wb_wrapperqsys : imx6_wb_wrapper_qsys
    port map (
            -- pcie connection
            refclk_clk => refclk_clk,
            hip_serial_tx_out0 => hip_serial_tx_out0,
            hip_serial_rx_in0 => hip_serial_rx_in0,
            npor_pin_perst => npor_pin_perst,
            npor_npor => npor_npor,
            -- candroutput
            gls_rst_reset => reset,
            gls_clk_clk => clk,
            -- irq
            irq_irq => irq_irq,
            -- aval64
            aval_exp_waitrequest => waitrequest_next_s,
            aval_exp_address => wbm_address,
            aval_exp_write => aval_exp_write,
            aval_exp_read => aval_exp_read,
            aval_exp_byteenable => wbm_byte_enable,
            aval_exp_readdatavalid => wbm_readvalid_s,
            aval_exp_writedata => wbm_writedata,
            aval_exp_readdata => wbm_readdata
    );

    waitrequest_next_s <= '1' when (bus_enable ='1' and wbm_ack = '0') else '0';

    wbm_readvalid_s <= (aval_exp_read and wbm_ack);
    bus_enable <= aval_exp_read or aval_exp_write;
    wbm_cycle  <= bus_enable;
    wbm_strobe <= bus_enable;
    wbm_write  <= bus_enable and aval_exp_write;

end architecture RTL;
