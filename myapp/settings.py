DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kidsplayground',
        'USER': 'jam',
        'PASSWORD': '1221',
        'HOST': 'localhost',
        'PORT': '3306',
        'TEST': {
            'NAME': 'test_kidsplayground',  # テスト用データベース名を指定
        },
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',  # これを追加
    'django.contrib.auth',          # これも必要
    'django.contrib.sessions',      # 必要に応じて追加
    'myapp',                        # 自分のアプリケーション
]

ROOT_URLCONF = 'myapp.urls'  # プロジェクトのURL設定ファイルを指定