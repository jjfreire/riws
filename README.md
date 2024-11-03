# riws

## How to use this repo

### Install chrome webdriver (necessary for selenium)
Go to https://developer.chrome.com/docs/chromedriver/downloads and find a compatible chromedriver.

1. Download compatible chromedriver-xxxxx.zip
2. Unzip it
3. Place the chromedriver binary in PATH

### Activate the venv
```bash
source venv/bin/activate
```

### ¿Por qué está presente o venv?
Porque se modificou o [middlewares.py](./venv/lib/python3.12/site-packages/scrapy_selenium/middlewares.py) da librería scrapy_selenium para que funcione con scrapy v4.Y.Z (https://stackoverflow.com/a/76608689)

https://github.com/JoeHO888/Geetest-Icon-CAPTCHA-Solving/blob/master/README.md

https://anti-captcha.com/apidoc/task-types/GeeTestTaskProxyless

### ElasticSearch

**Configuración ElasticSearch**

1. Descargar ElasticSearch: https://www.elastic.co/downloads/elasticsearch
2. Configuración de ElasticSearch: 
    - Edición do arquivo de configuración `elasticsearch.yml`:
        ```bash
        sudo nano /etc/elasticsearch/elasticsearch.yml 
        ```
    - Modificación das seguintes liñas: 
        ```bash
        # Enable security features
        xpack.security.enabled: false

        xpack.security.enrollment.enabled: false
        ```
3. Reinicio do servizo `elasticsearch.service`
    ```bash
    sudo systemctl restart elasticsearch.service 
    ```



**Uso da interface ElasticSearch-head**

1. Descarga do repositorio de elastic-head:
    ```bash
    git clone git://github.com/mobz/elasticsearch-head.git 
    ```
2. Configuración de `elasticsearch.yml` para permitir a comunicación:

    ```bash
    sudo nano /etc/elasticsearch/elasticsearch.yml 
    ```

    - Adición das seguintes liñas ao arquivo:

        ```bash
        # ---------------------------------- Various -----------------------------------
        http.cors.enabled: true

        http.cors.allow-origin: "*"

        ```

3. Reinicio do servizo `elasticsearch.service`
    ```bash
    sudo systemctl restart elasticsearch.service 
    ```
4. Execución de ElasticSearch-head:
Abrir nun navegador o arquivo index.html do repositorio clonado.
    
