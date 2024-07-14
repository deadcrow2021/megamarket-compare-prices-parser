def default_filter(text: str) -> str:
    text = text.lower().strip()
    return text


def filter_iphone(title: str) -> str:
    delete_chars = ['dual', 'esim', 'sim', '(', ')','ll', 'ja', 'eu', 'aa', 'hk', 'cn', 'tb', 'gb', '/']

    title = title.lower()

    for char in delete_chars:
        title = title.replace(char, '')
    

    title = title.replace('1024', '1')
    title = title.replace('  ', ' ')
    title = title.strip()
    
    if not title.startswith('apple'):
        title = 'apple ' + title
    
    return title


def filter_watch(title: str) -> str:
    title = title.lower()
    title = title.split('/')[0]
    title = title.strip()
    
    return title


def filter_mac(title: str) -> str:
    title = title.replace('/', ' ').replace('apple', '')
    title = title.strip()
    
    return title


def filter_samsung(title: str) -> str:
    title = title.lower()
    
    title = title.replace('/', ' ').replace('samsung', '').replace('galaxy', '')
    title = title.replace('flip', 'flip ').replace('fold', 'fold ')
    title = title.replace('  ', ' ').strip()
    
    return title


def filter_xiaomi(title: str) -> str:
    title = title.lower()
    
    title = title.replace('/', ' ').replace('xiaomi', '')#.replace('redmi', '').replace('poco', '')
    title = title.replace('  ', ' ').strip()
    
    return title


def filter_ps(title: str) -> str:
    title = title.lower()
    title = title.replace('  ', ' ').strip()
    
    return title


def filter_dyson(title: str) -> str:
    title = title.lower().replace('dyson', '').replace('/', ' ')
    title = title.replace('  ', ' ').strip()
    
    return title


def filter_ipad(title: str) -> str:
    title = title.lower().replace('apple', '')#.replace('ipad', '')
    title = title.replace('  ', ' ').strip()
    
    return title