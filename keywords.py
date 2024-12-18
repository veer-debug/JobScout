import spacy
import pdfplumber

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

SKILL_KEYWORDS = [
    "Machine Learning", "Data Science", "Python", "R", "SQL", "Data Analysis", "Deep Learning", "AI", "NLP",
    "Computer Vision", "Statistical Analysis", "Predictive Modeling", "Data Visualization", "Big Data",
    "Data Mining", "Regression Analysis", "Classification Algorithms", "Feature Engineering", "Time Series Analysis",
    "TensorFlow", "Keras", "Scikit-Learn", "Hadoop", "Spark", "MapReduce", "AWS", "GCP", "Azure", "SQL Server",
    "MySQL", "NoSQL Databases", "MongoDB", "PostgreSQL", "Cassandra", "Oracle", "Data Architecture", "ETL Tools",
    "Data Cleaning", "Data Transformation", "Data Integration", "Data Privacy", "Data Security", "Data Compliance",
    "Data Ethics", "Data Preprocessing", "Dimensionality Reduction", "PCA", "Random Forests", "Gradient Boosting",
    "SVM", "Logistic Regression", "Decision Trees", "Neural Networks", "Deep Learning Models", "Reinforcement Learning",
    "Bayesian Networks", "Graph Theory", "Optimization Algorithms", "Simulated Annealing", "Genetic Algorithms",
    "Natural Language Processing", "Text Mining", "Word Embeddings", "BERT", "GPT-3", "Transformer Models", "LSTM",
    "Long Short-Term Memory Networks", "Sequence Models", "Time Series Analysis", "Statistical Models", "Cryptocurrency",
    "Blockchain Development", "Smart Contracts", "Tokenomics", "Decentralized Finance", "Crypto Portfolio Management",
    "AI in Healthcare", "AI in Finance", "AI in Retail", "AI in Education", "AI in Smart Cities", "AI in Cybersecurity",
    "AI in Robotics", "AI in Autonomous Systems", "AI in the Automotive Industry", "AI in Supply Chain Management",
    "AI in Quality Control", "AI in Predictive Analytics", "AI in Image Analysis", "AI in Video Analysis",
    "AI in Natural Language Processing", "AI in Speech Recognition", "AI in Text Recognition", "AI in Object Detection",
    "AI in Facial Recognition", "AI in Gesture Recognition", "AI in Voice Recognition", "AI in Cyber Threat Detection",
    "AI in Autonomous Systems", "AI in Smart Grids", "AI in Home Automation", "AI in Internet of Things",
    "AI in Digital Twins", "AI in Smart Manufacturing",
    
    # Tech Marketing
    "Content Marketing", "SEO", "SEM", "PPC", "Social Media Marketing", "Email Marketing", "Affiliate Marketing",
    "Influencer Marketing", "Brand Strategy", "Market Research", "User Acquisition", "Customer Retention", "Analytics",
    "A/B Testing", "Conversion Rate Optimization", "Growth Hacking", "Paid Media Advertising", "Campaign Management",
    
    # Design
    "UI/UX Design", "Graphic Design", "Adobe Photoshop", "Adobe Illustrator", "Figma", "Sketch", "User Experience",
    "User Interface Design", "Wireframing", "Prototyping", "Color Theory", "Typography", "Motion Graphics",
    "Video Editing", "3D Design", "User Interface Animation", "Design Systems", "Agile UX", "Usability Testing",
    "Responsive Design", "Mobile Design", "Web Design"
]

class SkillExtractor:
    @staticmethod
    def extract_skills_from_text(text, skill_keywords=None):
        if skill_keywords is None:
            skill_keywords = SKILL_KEYWORDS
        doc = nlp(text)
        skills = [ent.text for ent in doc.ents if ent.text in skill_keywords]
        return skills
    
    @staticmethod
    def extract_skills_from_pdf(file_path, skill_keywords=None):
        if skill_keywords is None:
            skill_keywords = SKILL_KEYWORDS
        text = ''
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return SkillExtractor.extract_skills_from_text(text, skill_keywords)
