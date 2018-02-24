def includeme(config):
    config.add_route('users', '/lbc_scraper_admin/users')

    config.add_route('alerts', '/lbc_scraper_admin/users/{id_user}/alerts')
