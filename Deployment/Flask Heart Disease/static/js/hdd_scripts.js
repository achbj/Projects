// Function to generate PDF from the hdd_results section
function generatePDF() {
  // Check if jsPDF is defined
  if (typeof jsPDF !== "undefined") {
    const element = document.querySelector(".hdd_results");

    html2canvas(element, {
      onrendered: function (canvas) {
        const pdf = new jsPDF();
        pdf.addImage(
          canvas.toDataURL("image/png"),
          "PNG",
          0,
          0,
          pdf.internal.pageSize.getWidth(),
          pdf.internal.pageSize.getHeight()
        );
        pdf.save("hdd_results.pdf");
      },
    });
  } else {
    // If jsPDF is not defined, log an error message
    console.error("jsPDF is not defined");
  }
}

// Call generatePDF function when the page is loaded
document.addEventListener("DOMContentLoaded", function (event) {
  generatePDF();
});
