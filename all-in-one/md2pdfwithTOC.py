import subprocess

def convert_md_to_pdf_with_toc(md_file_path, pdf_file_path):
    # Command to convert Markdown to PDF with pandoc
    # This command includes options for:
    # -s: standalone document
    # --toc: include a table of contents
    # --toc-depth: specify the depth of the TOC, adjust as needed
    # -o: output file
    # Additional LaTeX options can be included with `-V` for customizing the PDF
    command = [
        'pandoc', md_file_path, '-s', '--toc', '--toc-depth=2', '--pdf-engine=xelatex', '-o', pdf_file_path
    ]
    
    # Execute the pandoc command
    try:
        subprocess.run(command, check=True)
        print(f"Conversion successful. PDF saved to: {pdf_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

# Example usage
md_file_path = 'all.gpt-4-1106-preview.chinese.md'
pdf_file_path = '540bookSummaryChinese.pdf'
convert_md_to_pdf_with_toc(md_file_path, pdf_file_path)

