import os
import requests
import re
from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup
import time

# --- Course Data ---
courses = {
    "CS224N_NLP": [
        {
            "title": "Lecture 01 - Word Vectors",
            "slides": "https://web.stanford.edu/class/cs224n/slides_w25/cs224n-2025-lecture01-wordvecs1.pdf",
            "notes": "https://web.stanford.edu/class/cs224n/readings/cs224n_winter2023_lecture1_notes_draft.pdf"
        },
        {
            "title": "Lecture 02 - Word Vectors and Language Models",
            "slides": "https://web.stanford.edu/class/cs224n/slides_w25/cs224n-2025-lecture02-wordvecs2.pdf",
            "notes": "https://web.stanford.edu/class/cs224n/readings/cs224n-2019-notes02-wordvecs2.pdf"
        },
         {
            "title": "Lecture 03 - Backprop and Neural Networks",
            "slides": "https://web.stanford.edu/class/cs224n/slides_w25/cs224n-2025-lecture03-neuralnets.pdf",
            "notes": "https://web.stanford.edu/class/cs224n/readings/cs224n-2019-notes03-neuralnets.pdf"
        },
        {
            "title": "Lecture 04 - Dependency Parsing",
            "slides": "https://web.stanford.edu/class/cs224n/slides_w25/cs224n-2025-lecture04-dep-parsing.pdf",
            "notes": "https://web.stanford.edu/class/cs224n/readings/cs224n-2019-notes04-dependencyparsing.pdf"
        },
        {
            "title": "Lecture 05 - RNNs and Language Models",
            "slides": "https://web.stanford.edu/class/cs224n/slides_w25/cs224n-2025-lecture05-rnnlm.pdf",
            "notes": "https://web.stanford.edu/class/cs224n/readings/cs224n-2019-notes05-LM_RNN.pdf"
        },
        {
            "title": "Lecture 06 - Advanced RNNs",
            "slides": "https://web.stanford.edu/class/cs224n/slides_w25/cs224n-2025-lecture06-fancy-rnn.pdf",
             "notes": "https://web.stanford.edu/class/cs224n/readings/cs224n-2019-notes05-LM_RNN.pdf"
        },
        {
             "title": "Lecture 07 - Final Projects",
             "slides": "https://web.stanford.edu/class/cs224n/slides_w25/cs224n-2025-lecture07-final-project.pdf",
             "notes": None
        },
        {
            "title": "Lecture 08 - Transformers",
            "slides": "https://web.stanford.edu/class/cs224n/slides_w25/cs224n-2025-lecture08-transformers.pdf",
            "notes": "https://web.stanford.edu/class/cs224n/readings/cs224n-self-attention-transformers-2023_draft.pdf"
        },
        {
            "title": "Lecture 09 - Pretraining",
             "slides": "https://web.stanford.edu/class/cs224n/slides_w25/cs224n-2025-lecture09-pretraining.pdf",
             "notes": None
        },
        {
            "title": "Lecture 10 - Post-training (RLHF)",
             "slides": "https://web.stanford.edu/class/cs224n/slides_w25/cs224n-2025-lecture10-instruction-tunining-rlhf.pdf",
             "notes": None
        },
        {
            "title": "Lecture 11 - Efficient Adaptation",
             "slides": "https://web.stanford.edu/class/cs224n/slides_w25/cs224n-2025-lecture11-adapatation.pdf",
             "notes": None
        },
        {
            "title": "Lecture 12 - Evaluation",
             "slides": "https://web.stanford.edu/class/cs224n/slides_w25/cs224n-2025-lecture12-evaluation-final.pdf",
             "notes": None
        },
        {
            "title": "Lecture 13 - Question Answering",
             "slides": "https://web.stanford.edu/class/cs224n/slides_w25/cs224n-2025-lecture13-QA.pdf",
             "notes": None
        },
        {
             "title": "Lecture Guest - Interpretability",
             "slides": "https://web.stanford.edu/class/cs224n/slides_w25/cs224n-2025-guest-lecture-interpretability.pdf",
             "notes": None
        }
    ],
    "CS231n_Vision": [
        { "title": "Lecture 01 - Introduction", "slides": "https://cs231n.stanford.edu/slides/2025/lecture_1_part_1.pdf" },
        { "title": "Lecture 02 - Linear Classification", "slides": "https://cs231n.stanford.edu/slides/2025/lecture_2.pdf", "notes": "https://cs231n.github.io/linear-classify/" },
        { "title": "Lecture 03 - Optimization", "slides": "https://cs231n.stanford.edu/slides/2025/lecture_3.pdf", "notes": "https://cs231n.github.io/optimization-1/" },
        { "title": "Lecture 04 - Backpropagation", "slides": "https://cs231n.stanford.edu/slides/2025/lecture_4.pdf", "notes": "http://cs231n.github.io/optimization-2" },
        { "title": "Lecture 05 - CNNs", "slides": "https://cs231n.stanford.edu/slides/2025/lecture_5.pdf", "notes": "http://cs231n.github.io/convolutional-networks" },
        { "title": "Lecture 06 - CNN Architectures", "slides": "https://cs231n.stanford.edu/slides/2025/lecture_6.pdf" },
        { "title": "Lecture 07 - RNNs", "slides": "https://cs231n.stanford.edu/slides/2025/lecture_7.pdf" },
        { "title": "Lecture 08 - Attention and Transformers", "slides": "https://cs231n.stanford.edu/slides/2025/lecture_8.pdf" },
        { "title": "Lecture 09 - Object Detection", "slides": "https://cs231n.stanford.edu/slides/2025/lecture_9.pdf" },
        { "title": "Lecture 10 - Video Understanding", "slides": "https://cs231n.stanford.edu/slides/2025/lecture_10.pdf" },
        { "title": "Lecture 11 - Distributed Training", "slides": "https://cs231n.stanford.edu/slides/2025/lecture_11.pdf" },
        { "title": "Lecture 12 - Self-supervised Learning", "slides": "https://cs231n.stanford.edu/slides/2025/lecture_12.pdf" },
        { "title": "Lecture 13 - Generative Models 1", "slides": "https://cs231n.stanford.edu/slides/2025/lecture_13.pdf" },
        { "title": "Lecture 14 - Generative Models 2", "slides": "https://cs231n.stanford.edu/slides/2025/lecture_14.pdf" },
        { "title": "Lecture 15 - 3D Vision", "slides": "https://cs231n.stanford.edu/slides/2025/lecture_15.pdf" },
         { "title": "Lecture 16 - Vision and Language", "slides": "https://cs231n.stanford.edu/slides/2025/lecture_16.pdf" },
         { "title": "Lecture 17 - Robot Learning", "slides": "https://cs231n.stanford.edu/slides/2025/lecture_17.pdf" },
    ],
    "CS229_MachineLearning": [
        { "title": "Lecture 01 - Introduction", "notes": "http://cs229.stanford.edu/main_notes.pdf" },
        { "title": "Lecture 02 - Supervised Learning", "notes": "http://cs229.stanford.edu/notes2021fall/cs229-notes1.pdf" },
        { "title": "Lecture 03 - GDA and Naive Bayes", "notes": "http://cs229.stanford.edu/notes2021fall/cs229-notes2.pdf" },
        { "title": "Lecture 04 - SVMs", "notes": "http://cs229.stanford.edu/notes2021fall/cs229-notes3.pdf" },
        { "title": "Lecture 05 - Regularization", "notes": "http://cs229.stanford.edu/notes2021fall/cs229-notes4.pdf" },
        { "title": "Lecture 06 - Error Analysis", "notes": "http://cs229.stanford.edu/notes2021fall/cs229-notes5.pdf" },
         { "title": "Lecture 07 - Deep Learning Intro", "notes": "http://cs229.stanford.edu/notes2021fall/cs229-notes-deep-learning.pdf" },
          { "title": "Lecture 08 - EM Algorithm", "notes": "http://cs229.stanford.edu/notes2021fall/cs229-notes8.pdf" },
           { "title": "Lecture 09 - PCA", "notes": "http://cs229.stanford.edu/notes2021fall/cs229-notes10.pdf" },
           { "title": "Lecture 10 - ICA", "notes": "http://cs229.stanford.edu/notes2021fall/cs229-notes11.pdf" },
           { "title": "Lecture 11 - RL", "notes": "http://cs229.stanford.edu/notes2021fall/cs229-notes12.pdf" },
    ],
     "CS224W_Graphs": [
    { "title": "Lecture 01 - Introduction", "slides": "https://web.stanford.edu/class/cs224w/slides/01-intro.pdf", "notes": "https://archives.leni.sh/stanford/CS224w.pdf" },
    { "title": "Lecture 02 - Node Embeddings", "slides": "https://web.stanford.edu/class/cs224w/slides/02-nodeemb.pdf" },
    { "title": "Lecture 03 - GNNs", "slides": "https://web.stanford.edu/class/cs224w/slides/03-GNN1.pdf" },
    { "title": "Lecture 04 - GNN Perspective", "slides": "https://web.stanford.edu/class/cs224w/slides/04-GNN2.pdf" },
    { "title": "Lecture 05 - GNN Training", "slides": "https://web.stanford.edu/class/cs224w/slides/05-GNN3.pdf" },
    { "title": "Lecture 06 - Theory of GNNs", "slides": "https://web.stanford.edu/class/cs224w/slides/06-theory.pdf" },
    { "title": "Lecture 07 - Graph Encoders", "slides": "https://web.stanford.edu/class/cs224w/slides/07-theory2.pdf" },
    { "title": "Lecture 08 - Graph Transformers", "slides": "https://web.stanford.edu/class/cs224w/slides/08-graph-transformer1.pdf" },
    { "title": "Lecture 09 - Heterogenous Graphs", "slides": "https://web.stanford.edu/class/cs224w/slides/09-hetero.pdf" },
    { "title": "Lecture 10 - Knowledge Graphs", "slides": "https://web.stanford.edu/class/cs224w/slides/10-kg.pdf" },
    { "title": "Lecture 11 - RecSys", "slides": "https://web.stanford.edu/class/cs224w/slides/11-recsys.pdf" },
    { "title": "Lecture 12 - Relational DL", "slides": "https://web.stanford.edu/class/cs224w/slides/12-RDL.pdf" },
    { "title": "Lecture 13 - Advanced RDL", "slides": "https://web.stanford.edu/class/cs224w/slides/13-Advanced_topics_RDL.pdf" },
    { "title": "Lecture 14 - Advanced GNNs", "slides": "https://web.stanford.edu/class/cs224w/slides/14-advanced_gnns.pdf" },
    { "title": "Lecture 15 - KG Foundation Models", "slides": "https://web.stanford.edu/class/cs224w/slides/15-KGFoundationModels.pdf" },
    { "title": "Lecture 16 - LLM + GNN", "slides": "https://web.stanford.edu/class/cs224w/slides/Lecture16.pdf" },
    { "title": "Lecture 17 - Agents", "slides": "https://web.stanford.edu/class/cs224w/slides/2025-cs224w-lecture.pdf" },
    { "title": "Lecture 18 - Deep Gen for Graphs", "slides": "https://web.stanford.edu/class/cs224w/slides/18-deep-generation.pdf" },
    ],
    "CS324_LLMs": [
    { "title": "01 Introduction", "notes": "https://stanford-cs324.github.io/winter2022/lectures/introduction" },
    { "title": "02 Capabilities", "notes": "https://stanford-cs324.github.io/winter2022/lectures/capabilities" },
    { "title": "03 Harms I", "notes": "https://stanford-cs324.github.io/winter2022/lectures/harms-1" },
    { "title": "04 Harms II", "notes": "https://stanford-cs324.github.io/winter2022/lectures/harms-2" },
    { "title": "05 Data", "notes": "https://stanford-cs324.github.io/winter2022/lectures/data" },
    { "title": "06 Security", "notes": "https://stanford-cs324.github.io/winter2022/lectures/security" },
    { "title": "07 Legality", "notes": "https://stanford-cs324.github.io/winter2022/lectures/legality" },
    { "title": "08 Modeling", "notes": "https://stanford-cs324.github.io/winter2022/lectures/modeling" },
    { "title": "09 Training", "notes": "https://stanford-cs324.github.io/winter2022/lectures/training" },
    { "title": "10 Parallelism", "notes": "https://stanford-cs324.github.io/winter2022/lectures/parallelism" },
    { "title": "11 Scaling Laws", "notes": "https://stanford-cs324.github.io/winter2022/lectures/scaling-laws" },
    { "title": "12 Architectures", "notes": "https://stanford-cs324.github.io/winter2022/lectures/selective-architectures" },
    { "title": "13 Adaptation", "notes": "https://stanford-cs324.github.io/winter2022/lectures/adaptation" },
    ],
    "CS25_Transformers": [
     { "title": "Course Link", "notes": "https://web.stanford.edu/class/cs25/" }
    ]
}

def clean_filename(s):
    return re.sub(r'[\\/*?:"<>|]', "", s).replace(" ", "_")

def download_file(url, filepath):
    if not url: return
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {filepath}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def html_to_markdown(url, filepath):
    if not url: return
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Basic extraction: Title, and then text
        markdown = f"# Reference: {url}\n\n"
        
        # Try to find the main content
        content = soup.find('main') or soup.find('article') or soup.find('div', class_='content') or soup.body
        
        if content:
             for tag in content.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol', 'li', 'pre', 'code']):
                if tag.name == 'h1': markdown += f"# {tag.get_text().strip()}\n\n"
                elif tag.name == 'h2': markdown += f"## {tag.get_text().strip()}\n\n"
                elif tag.name == 'h3': markdown += f"### {tag.get_text().strip()}\n\n"
                elif tag.name == 'p': markdown += f"{tag.get_text().strip()}\n\n"
                elif tag.name == 'li': markdown += f"- {tag.get_text().strip()}\n"
                elif tag.name == 'pre': markdown += f"```\n{tag.get_text()}\n```\n\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"Saved notes: {filepath}")
        
    except Exception as e:
        print(f"Failed to convert {url}: {e}")

base_dir = r"f:\learnbydoingwithsteven\stanford\20251226_latest_courses"
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

for course_name, lectures in courses.items():
    course_dir = os.path.join(base_dir, course_name)
    if not os.path.exists(course_dir):
        os.makedirs(course_dir)
    
    print(f"Processing {course_name}...")
    
    for lec in lectures:
        title = lec.get('title', 'Unknown')
        lec_dir = os.path.join(course_dir, clean_filename(title))
        if not os.path.exists(lec_dir):
            os.makedirs(lec_dir)
        
        # Download Slides
        slides_url = lec.get('slides')
        if slides_url:
            filename = os.path.basename(unquote(urlparse(slides_url).path))
            if not filename.endswith('.pdf'): filename += ".pdf"
            download_file(slides_url, os.path.join(lec_dir, filename))
        
        # Download Notes
        notes_url = lec.get('notes')
        if notes_url:
            if notes_url.endswith('.pdf'):
                filename = os.path.basename(unquote(urlparse(notes_url).path))
                if not filename.endswith('.pdf'): filename += ".pdf"
                download_file(notes_url, os.path.join(lec_dir, filename))
            else:
                # Assume HTML
                html_to_markdown(notes_url, os.path.join(lec_dir, "notes.md"))
        
        time.sleep(0.5) # Be nice to the server

print("Done!")
