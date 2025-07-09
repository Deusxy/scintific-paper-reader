"""
Sample text generator for testing the NaturalReader Clone
Run this to create a sample PDF for testing purposes.
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def create_sample_pdf():
    filename = "data/sample_document.pdf"
    
    # Create a simple PDF with sample text
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Sample content
    content = [
        "The Future of Artificial Intelligence",
        "",
        "Artificial intelligence has become one of the most transformative technologies of our time. Machine learning algorithms are now capable of processing vast amounts of data and making predictions with remarkable accuracy.",
        "",
        "Natural language processing has advanced to the point where computers can understand and generate human-like text. This technology enables applications like chatbots, translation services, and automated content creation.",
        "",
        "Computer vision systems can now recognize objects, faces, and scenes with superhuman accuracy. These systems are being used in autonomous vehicles, medical imaging, and security applications.",
        "",
        "The integration of AI into everyday life continues to accelerate. From smart home devices to personalized recommendations, AI is making our lives more convenient and efficient.",
        "",
        "However, the rapid advancement of AI also raises important questions about ethics, privacy, and the future of work. It is crucial that we develop these technologies responsibly and consider their impact on society.",
        "",
        "As we look to the future, AI will likely become even more integrated into our daily lives. The key is to harness its power while addressing the challenges it presents."
    ]
    
    story = []
    for line in content:
        if line.strip():
            p = Paragraph(line, styles['Normal'])
            story.append(p)
        story.append(Spacer(1, 12))
    
    doc.build(story)
    print(f"Sample PDF created: {filename}")

if __name__ == "__main__":
    try:
        create_sample_pdf()
    except ImportError:
        print("reportlab not installed. Creating simple text version instead.")
        with open("data/sample_text.txt", "w") as f:
            f.write("""The Future of Artificial Intelligence

Artificial intelligence has become one of the most transformative technologies of our time. Machine learning algorithms are now capable of processing vast amounts of data and making predictions with remarkable accuracy.

Natural language processing has advanced to the point where computers can understand and generate human-like text. This technology enables applications like chatbots, translation services, and automated content creation.

Computer vision systems can now recognize objects, faces, and scenes with superhuman accuracy. These systems are being used in autonomous vehicles, medical imaging, and security applications.

The integration of AI into everyday life continues to accelerate. From smart home devices to personalized recommendations, AI is making our lives more convenient and efficient.

However, the rapid advancement of AI also raises important questions about ethics, privacy, and the future of work. It is crucial that we develop these technologies responsibly and consider their impact on society.

As we look to the future, AI will likely become even more integrated into our daily lives. The key is to harness its power while addressing the challenges it presents.""")
        print("Sample text file created: data/sample_text.txt")
