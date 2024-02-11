from fpdf import FPDF

def main():
    inp = input("Name: ")
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "CS50 Shirtificate", border = 0, align='C')
    pdf.image("shirtificate.png", y=60, x=80)
    string = inp + " took CS50"
    pdf.cell(0, 40, string, align="C" )
    pdf.output("shirtificate.pdf")

main()