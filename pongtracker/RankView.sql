CREATE 
    ALGORITHM = UNDEFINED
    SQL SECURITY DEFINER
VIEW `Statistics_rankView` AS
    select 
        `r`.`_user_id` AS `id`,
        round((`r`.`_mu` - (3 * `r`.`_sigma`)), 5) AS `_skillNumber`
    from
        `Statistics_ranking` `r`
    order by (`r`.`_mu` - (3 * `r`.`_sigma`)) desc
