# riws

## How to use this repo

### 1. Install the required dependencies

#### 1.1. Python 3.12

https://www.python.org/downloads/

This is not strictly necessary, but we recommend it due to libraries compatibilies.

#### 1.2. Chrome browser (necessary for selenium)

https://support.google.com/chrome/answer/95346?hl=en&co=GENIE.Platform%3DDesktop

#### 1.3. ChromeDriver (necessary for selenium)

Go to https://developer.chrome.com/docs/chromedriver/downloads and find a compatible ChromeDriver.

1. Download compatible chromedriver-xxxxx.zip
2. Unzip it
3. Place the chromedriver binary in PATH

#### 1.4. Create the venv and install the necessary libraries

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp middlewares.py venv/lib/python3.12/site-packages/scrapy_selenium/middlewares.py # Read note
```

Note: Why is this moddification necessary? It is a [workaround implementation](https://github.com/clemfromspace/scrapy-selenium/blob/5c3fe7b43ab336349ef5fdafe39fc87f6a8a8c34/scrapy_selenium/middlewares.py) for this open [issue](https://github.com/clemfromspace/scrapy-selenium/issues/128). Discovered [here](https://stackoverflow.com/a/76608689).

#### 1.5. Docker engine

https://docs.docker.com/engine/install/

### 2. Run the spider

First of all, you can configure how many InfoJobs pages you want to proccess in [config.json](./RIWS/RIWS/config.json) file. Max value is hardcoded to 400, so max_pages must be <=400. Then, execute:

```bash
cd RIWS/RIWS
scrapy crawl jobs_spider # Make sure your venv is still activated
```

TODO: Explain how to solve the captcha (when prompted) with screenshots.

This will create a jobs.json file, that contains the documents to be indexed in Elasticsearch.

### 3. Run Elasticsearch and frontend containers

First of all, place the jobs.json file in run/index-initializer/jobs.json. There is already an example file with 8932 documents, just overwrite it if you want to.

Then, execute:
```bash
cd run
docker compose up
```

This will automatically launch a Elasticsearch container and index the documents using an auxiliary container (index-initializer). Also, a frontend container will be launched in your localhost:3000 port ready to proccess requests.

Wait for this message to be desplayed in your terminal: `index-initializer   | Document insertion finished. Access http://localhost:3000`

Then, access [http://localhost:3000](http://localhost:3000) in your web browser.

### 4. Stop Elasticsearch and frontend containers

```bash
cd run
docker compose down
```

## FAQ
### Why is Selenium necessary?

Because of dynamic content loading and captcha solving. Without Selenium we wouldn't be able to fetch the jobs.

### Why not more than 400 pages? Hardcoded value in [quotes_spider.py](./RIWS/RIWS/spiders/quotes_spider.py), line 32

Retrieving the jobs would be time-consuming, unnecessary, and could also introduce additional issues with CAPTCHAs.

## License
This project is licensed under the **Custom Non-Commercial License**. It may be used for educational and research purposes only. Commercial use is prohibited without explicit written consent from the contributors. See the [LICENSE](./LICENSE) file for more details.
