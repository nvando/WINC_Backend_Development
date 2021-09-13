# Do not modify these lines
__winc_id__ = "d0d3cdcefbb54bc980f443c04ab3a9eb"
__human_name__ = "operators"

# Add your code after this line


# The language spoken the most in Switzerland is the same as in Spain.
sz_populair_language = "German"
sp_populair_language = "Castilian Spanish"
print(sz_populair_language == sp_populair_language)

# The most prevalent religion in Switzerland is the same as in Spain.
sz_populair_religion = "Roman Catholic"
sp_populair_religion = "Roman Catholic"
print(sz_populair_religion == sz_populair_religion)

# The name length of Spain's capital does not equal that of Switzerland.
sz_capital = "Bern"
sp_capital = "Madrid"
print(len(sz_capital) != len(sp_capital))

# Switzerland's GDP is greater than Spain's GDP.
sz_gdp = 580
sp_gdp = 1778000
print(sz_gdp > sp_gdp)

# The population growth is less than 1% in Switzerland and Spain.
sz_population_growth = 0.66
sp_population_growth = 0.67
print(sz_population_growth < 1 and sp_population_growth < 1)

# At least one of the two countries has a population count of over 10 million.
sz_population_count = 8.4
sp_population_count = 50
print(sz_population_count > 10 or sp_population_count > 10)

# Exactly one of the two countries has a population count of over 10 million.
print(
    (sz_population_count > 10 and sp_population_count < 10)
    or (sz_population_count < 10 and sp_population_count > 10)
)
