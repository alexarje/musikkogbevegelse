// Insert a 'Download PDF' link into the download dropdown that points to the LaTeX-built PDF
(function () {
  try {
    var menu = document.querySelector('.dropdown-download-buttons .dropdown-menu');
    if (!menu) return;
    var li = document.createElement('li');
    var a = document.createElement('a');
    a.className = 'btn btn-sm dropdown-item';
    a.href = '_static/MusikkOgBevegelse.pdf';
    a.target = '_blank';
    a.title = 'Download LaTeX PDF';
    a.innerHTML = '<span class="btn__icon-container"><i class="fas fa-file-pdf"></i></span><span class="btn__text-container">LaTeX PDF</span>';
    li.appendChild(a);
    menu.appendChild(li);
  } catch (e) {
    // silent fail; best-effort enhancement
    console && console.warn && console.warn('download_pdf.js failed', e);
  }
})();
