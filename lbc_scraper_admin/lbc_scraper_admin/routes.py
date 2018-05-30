def includeme(config):
    config.add_route('users', '/lbc_scraper_admin/users')

    config.add_route('alerts', '/lbc_scraper_admin/users/{id_user}/alerts')
    config.add_route('alert', '/lbc_scraper_admin/users/{id_user}/alert/{id_alert}')

    config.add_route('new_alert', '/lbc_scraper_admin/users/{id_user}/new_alert')

    config.add_route('home', '/')
    config.add_route('hello', '/howdy')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

