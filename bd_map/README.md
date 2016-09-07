Source files:

- bd_raw_down.py: read lexicon files and search baidu using each line, and write output json per line (multiline json is joined)
- bd_detail_gen.py: read raw json output per line, and write the detail url
- bd_detail_crawler.py: crawl the detail page of baidu poi
- find_fallback.sh: find the failed crawling
- bd_extract_further_link.py: extract links to other sources like dianping from every baidu detail page
- bd_further_crawler.py: crawl html pages following the further 3rd-party links
