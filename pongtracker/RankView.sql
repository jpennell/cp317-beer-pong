CREATE 
    ALGORITHM = UNDEFINED
    SQL SECURITY DEFINER
VIEW `Statistics_rankView` AS
    select 
		`r`.`_user_id` AS `id`,
		round((`r`.`_mu` - (3 * `r`.`_sigma`)), 5) AS `_skillNumber`,
		(`s`.`_cup1Sunk` + `s`.`_cup2Sunk` + 
		 `s`.`_cup3Sunk` + `s`.`_cup4Sunk` + 
		 `s`.`_cup5Sunk` + `s`.`_cup6Sunk`) AS `cups`
	from
		`Statistics_ranking` `r`, 
		`Statistics_lifestats` `s`
	where `r`.`id` = `s`.`id`
	order by 
		(`r`.`_mu` - (3 * `r`.`_sigma`)) desc,
		`cups` desc