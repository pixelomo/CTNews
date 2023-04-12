$(document).ready(function () {
    tinymce.init({
        selector: "#translation-editor",
        height: '100vh',
        plugins: 'anchor autolink code charmap codesample image link lists media searchreplace table wordcount',
        toolbar: 'undo redo | fontfamily fontsize | bold italic underline strikethrough | link image media table | align lineheight | numlist bullist indent outdent | charmap | removeformat | code',
        menubar: 'tools',
        content_style: 'img { max-width: 100% !important; } .mce-content-body { padding-bottom: 6rem !important; }'
    });

    function loadArticles() {
        $.getJSON("/api/get_all_articles", function (data) {
            $("#article-list").empty();
            data.forEach(function (article) {
                $("<li>")
                    .addClass("list-group-item")
                    .text(article.title)
                    .data("article", article)
                    .on("click", function (event) {
                        onArticleClick(event);

                        $("#original-title").html(article.title);
                        $("#original-html").html(article.html);
                        tinymce.get("translation-editor").setContent(article.content_translated || '');
                    })
                    .appendTo("#article-list");
            });
        });
    }

    loadArticles();

    // const sidebar = document.querySelector(".sidebar");
    // const sidebarToggle = document.querySelector("#sidebar-toggle");

    // sidebarToggle.addEventListener("click", function () {
    //     sidebar.classList.toggle("minimized");
    //     sidebarToggle.textContent = sidebar.classList.contains("minimized")
    //     ? "Show"
    //     : "Hide";
    // });

    function onArticleClick(event) {
        // Remove the selected-article class from the previously selected article
        const previousSelectedArticle = document.querySelector(".selected-article");
        if (previousSelectedArticle) {
            previousSelectedArticle.classList.remove("selected-article");
        }
        // Add the selected-article class to the clicked article
        const clickedArticle = event.target.closest("li");
        if (clickedArticle) {
            clickedArticle.classList.add("selected-article");
        }
    }


});


// tinymce.init({
//     selector: 'textarea',
//     plugins: 'anchor autolink charmap codesample emoticons image link lists media searchreplace table visualblocks wordcount',
//     toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table | align lineheight | numlist bullist indent outdent | emoticons charmap | removeformat',
//   });

// document.addEventListener('DOMContentLoaded', () => {
//     // Initialize TinyMCE editor
//     tinymce.init({
//       selector: '#translated-content',
//       plugins: 'anchor autolink charmap codesample image link lists media searchreplace table visualblocks wordcount',
//       toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table | align lineheight | numlist bullist indent outdent | charmap | removeformat',
//       setup: function (editor) {
//         editor.on('init', function () {
//           // Fetch the article data from your API
//           fetch('/api/get_all_articles')
//             .then((response) => response.json())
//             .then((articles) => {
//               // Display the original content and set the translated content in the TinyMCE editor
//               if (articles.length > 0) {
//                 const article = articles[0]; // Replace this with the article you want to display
//                 displayArticle(article); // Assumes you have a function called `displayArticle` that displays the original content
//                 editor.setContent(article.content_translated || ''); // Set the translated content in the TinyMCE editor
//               }
//             });
//         });
//       },
//     });

//     // Function to display the original content of the article
//     function displayArticle(article) {
//       // Assumes you have an element with the ID 'original-content' for displaying the original content
//       const originalContentElement = document.getElementById('original-content');
//       if (originalContentElement) {
//         originalContentElement.innerHTML = article.html || '';
//       }
//     }
//   });
