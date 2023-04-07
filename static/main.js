document.addEventListener('DOMContentLoaded', () => {
    // Initialize TinyMCE editor
    tinymce.init({
      selector: '#translated-content',
      plugins: 'anchor autolink charmap codesample image link lists media searchreplace table visualblocks wordcount',
      toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table | align lineheight | numlist bullist indent outdent | charmap | removeformat',
      setup: function (editor) {
        editor.on('init', function () {
          // Fetch the article data from your API
          fetch('/api/get_all_articles')
            .then((response) => response.json())
            .then((articles) => {
              // Display the original content and set the translated content in the TinyMCE editor
              if (articles.length > 0) {
                const article = articles[0]; // Replace this with the article you want to display
                displayArticle(article); // Assumes you have a function called `displayArticle` that displays the original content
                editor.setContent(article.content_translated || ''); // Set the translated content in the TinyMCE editor
              }
            });
        });
      },
    });

    // Function to display the original content of the article
    function displayArticle(article) {
      // Assumes you have an element with the ID 'original-content' for displaying the original content
      const originalContentElement = document.getElementById('original-content');
      if (originalContentElement) {
        originalContentElement.innerHTML = article.html || '';
      }
    }
  });
