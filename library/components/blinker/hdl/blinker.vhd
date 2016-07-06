library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.all;

Entity blinker is 
generic (
	NB_LEDS 	: natural := 1;
	prescaler 	: natural := 10000
);
port (
	rst_i		: in std_logic;
	clk_i		: in std_logic;
	output_o	: out std_logic_vector(NB_LEDS-1 downto 0)
);
end entity;

---------------------------------------------------------------------------
Architecture blinker_1 of blinker is
---------------------------------------------------------------------------
	signal output_s : std_logic_vector(NB_LEDS-1 downto 0);
	signal cpt_val_s : natural range 0 to prescaler-1;
	signal clk_s : std_logic;
	signal tick_s : std_logic;
begin
	output_o <= output_s;

	prescaler_proc : process(clk_i)
	begin
		if rising_edge(clk_i) then
			tick_s <= '0';
			if rst_i = '1' then
				cpt_val_s <= 0;
			else
				if cpt_val_s = prescaler - 1 then
					cpt_val_s <= 0;
					tick_s <= '1';
				else
					cpt_val_s <= cpt_val_s + 1;
				end if;
			end if;
		end if;
	end process;

	process(clk_s)
	begin
		if rising_edge(clk_i) then
			if rst_i = '1' then
				output_s <= (others => '0');
			else
				if (tick_s = '1') then
					output_s <= std_logic_vector(unsigned(output_s)+1);
				end if;
			end if;
		end if;
	end process;

end architecture blinker_1;

