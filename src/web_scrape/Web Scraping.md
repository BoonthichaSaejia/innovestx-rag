# 1.InnovestX Source
1. FAQs: https://www.innovestx.co.th/faqs
2. Product User Guide: https://www.innovestx.co.th/products/product-user-guide
3. Private Fund Assistance: https://www.innovestx.co.th/products/investment-advisor/private-fund

# 2.Scrape
Before scraping, please create and activate your virtual environment.
```bash
python3 -m venv innovestx-rag
source innovestx-rag/bin/activate
pip install -r requirements.txt
```

| Information | Abbriviation | Notebook | Type of Data |
| ----------- | ------------ | -------- | -------------|
| FAQs        | faq | [scrape_faqs.ipynb](src/web_scrape/scrape_faqs.ipynb) | Pairs of QA |
| Product User Guidelines | pug | [scrape_product_user_guideline.ipynb](src/web_scrape/scrape_product_user_guideline.ipynb) | Text and File containing text, link, img_url |
| Private Fund Assistance | pfa | [scrape_private_fund_asst.ipynb](src/web_scrape/scrape_private_fund_asst.ipynb) | Text and PDFs |

# 3. Information Extraction
Before embedding a certain type of data in each documents is chosen for the vector search

| Information | Embedding Text  | Actual text used for answer generatation |
| ----------- | --------------  | -----------------------------------------|
| FAQ         | question (text) | both question and answer extracted from doc.page_content and doc.metadata |
| PUG - text  | text content    | text context + important link + image_path from doc.page_content and doc.metadata |
| PUG - image | generated caption | image_path from doc.metadata |
| PFA - text  | text content    | text content from doc.page_content |
| PFA - pdf   | extracted text  | extracted text from doc.page_content |
 

