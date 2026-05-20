import urllib.request
import xml.etree.ElementTree as ET
import requests
import os
import json

class PaperAgent:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.pdf_dir = os.path.join(base_dir, "01_research", "papers", "pdf")
        self.api_url = "http://localhost:8000/api/v1/research/register"
        os.makedirs(self.pdf_dir, exist_ok=True)

    def fetch_arxiv_papers(self, query="stock price prediction", max_results=3):
        """arXiv APIから時系列・株価予測に関する最新論文を検索"""
        url = f"http://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(query)}&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
        
        try:
            response = urllib.request.urlopen(url)
            xml_data = response.read()
            return self._parse_arxiv_xml(xml_data)
        except Exception as e:
            print(f"[Error] Failed to fetch from arXiv: {e}")
            return []

    def _parse_arxiv_xml(self, xml_data):
        root = ET.fromstring(xml_data)
        namespaces = {'atom': 'http://www.w3.org/2005/Atom'}
        papers = []

        for entry in root.findall('atom:entry', namespaces):
            arxiv_id = entry.find('atom:id', namespaces).text.split('/abs/')[-1].split('v')[0]
            title = entry.find('atom:title', namespaces).text.strip().replace('\n', ' ')
            published = entry.find('atom:published', namespaces).text[:10]
            pdf_url = entry.find("atom:link[@title='pdf']", namespaces).attrib['href']
            
            authors = [author.find('atom:name', namespaces).text for author in entry.findall('atom:author', namespaces)]
            
            papers.append({
                "paper_id": arxiv_id,
                "title": title,
                "authors": ", ".join(authors),
                "published_date": published,
                "arxiv_url": pdf_url
            })
        return papers

    def download_pdf(self, paper):
        """PDFを指定ディレクトリに自律ダウンロード"""
        pdf_path = os.path.join(self.pdf_dir, f"{paper['paper_id']}.pdf")
        if os.path.exists(pdf_path):
            print(f"[Info] PDF already exists: {pdf_path}")
            return pdf_path

        try:
            print(f"[Download] Fetching PDF for: {paper['paper_id']}")
            urllib.request.urlretrieve(paper['arxiv_url'], pdf_path)
            return pdf_path
        except Exception as e:
            print(f"[Error] PDF Download failed: {e}")
            return None

    def register_to_core(self, paper):
        """FastAPIのメタデータ管理エンドポイントへ登録通知"""
        payload = {
            "paper_id": paper["paper_id"],
            "title": paper["title"],
            "arxiv_url": paper["arxiv_url"],
            "category": "prediction"
        }
        try:
            res = requests.post(self.api_url, json=payload)
            if res.status_code == 201:
                print(f"[Register] Success: {paper['paper_id']}")
            else:
                print(f"[Register] Failed with status {res.status_code}")
        except Exception as e:
            print(f"[Register] Core API Connection Error: {e}")

    def run_pipeline(self):
        print("[Start] paper_agent クローリング実行")
        papers = self.fetch_arxiv_papers()
        for paper in papers:
            pdf_path = self.download_pdf(paper)
            if pdf_path:
                self.register_to_core(paper)
        print("[End] paper_agent パイプライン完了")

if __name__ == "__main__":
    agent = PaperAgent("C:\\Users\\User\\Desktop\\AI\\stock_ai_org")
    agent.run_pipeline()
