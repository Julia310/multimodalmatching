

def add_categories(df):
    """
        Add category column to the cleaned Zalando or Gerry Weber / Tommy Hilfiger dataframe for later blocking procedure
    """
    for value in df['name'].iteritems():
        product = value[1].lower()
        if ('schuh' in product and not 'shirt' in product) or 'sneaker' in product or 'sandal' in product or 'ballerina' in product \
                or 'pantolette' in product or 'zehentrenner' in product or 'zehntrenner' in product or 'pump' in product or 'high heel' in product \
                or 'mokassin' in product or ('boot' in product and not 'shirt' in product) or 'espadrille' in product or 'loafer' in product \
                or 'stiefel' in product or ('runner' in product and not 'bade' in product) or 'slipper' in product:
            row = value[0]
            df.loc[row, 'category'] = 'Schuhe'
        elif 'kleid' in product:
            row = value[0]
            df.loc[row, 'category'] = 'Kleider'
        elif ('pullover' in product or 'hoodie' in product or 'sweatshirt' in product or ('sweat' in product and 'jacke' in product) \
                or 'strick' in product or 'strukturkaro'in product) and not \
                ('rock' in product or 'beanie' in product or 'socken' in product or 'shorts' in product):
            row = value[0]
            df.loc[row, 'category'] = 'Oberteile'
        elif 'jacke' in product or ('blazer' in product and not 'strukturkaro' in product) or 'parka' in product \
                or 'sakko' in product or 'coat' in product or 'mantel' in product or 'cardigan' in product \
                or 'weste' in product or 'windbreaker' in product or 'anorak' in product:
            row = value[0]
            df.loc[row, 'category'] = 'Jacken'
        elif 'rock' in product:
            row = value[0]
            df.loc[row, 'category'] = 'Röcke'
        elif 'string' in product or 'tanga' in product or 'slip' in product or 'bh' in product or 'trunk' in product\
                or 'bralette' in product or 'panties' in product or 'bustier' in product or 'unterhose' in product \
                or 'bikini' in product and ('hose' in product or 'top' in product or 'oberteil' in product):
            row = value[0]
            df.loc[row, 'category'] = 'Unterwäsche'
        elif ('shirt' in product or 'hemd' in product or 'bluse' in product or 'Longsleeve' in product \
                or 'oberteil' in product or 'tunika' in product or 'rugby polo' in product) \
                and not ('strampler' in product or 'pyjama' in product and 'set' in product or 'surf' in product or 'bikini' in product):
            row = value[0]
            df.loc[row, 'category'] = 'Oberteile'
        elif 'top' in product and not 'laptop' in product:
            row = value[0]
            df.loc[row, 'category'] = 'Tops'
        elif 'socken' in product or 'füßlinge' in product or 'strümpfe' in product or 'sock' in product:
            row = value[0]
            df.loc[row, 'category'] = 'Socken'
        elif ('hose' in product or 'pants' in product or 'shorts' in product or 'chino' in product or 'tights' in product\
                or 'eggings' in product or 'bermuda' in product or 'culotte' in product or 'capri' in product or 'pant' in product) \
                and not ('pyjama' in product and 'set' in product or 'panties' in product or 'pantolette' in product or 'bikini' in product):
            row = value[0]
            df.loc[row, 'category'] = 'Hosen'
            '''if 'denim' in product:
                df.loc[row, 'category'] = "Jeans"'''
        elif ('tasche' in product or 'rucksack' in product or 'ranzen' in product or 'bag' in product or 'geldbörse' in product or 'satchel' in product or 'tote' in product
              or 'etui' in product or 'kulturbeutel' in product or 'weekender' in product or 'reisezubehör' in product or 'slingpack' in product or 'denim' in product):
            row = value[0]
            df.loc[row, 'category'] = 'Tasche'
        elif 'jeans' in product or 'pocket in siebenachtel' in product:
            row = value[0]
            df.loc[row, 'category'] = 'Hosen'
        else:
            row = value[0]
            df.loc[row, 'category'] = 'Sonstiges'
