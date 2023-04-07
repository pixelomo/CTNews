$(document).ready(function () {
    tinymce.init({
        selector: "#translation-editor",
        height: 500,
    });

    function loadArticles() {
        $.getJSON("/api/get_all_articles", function (data) {
            $("#article-list").empty();
            data.forEach(function (article) {
                $("#article-list").append(
                    $("<li>")
                        .addClass("list-group-item")
                        .text(article.title)
                        .data("article", article)
                        .on("click", function () {
                            $("#original-html").html(article.html);
                            tinymce.get("translation-editor").setContent(article.content_translated || '');
                        })
                );
            });
        });
    }

    loadArticles();
});


// tinymce.init({
//     selector: 'textarea',
//     plugins: 'anchor autolink charmap codesample emoticons image link lists media searchreplace table visualblocks wordcount',
//     toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table | align lineheight | numlist bullist indent outdent | emoticons charmap | removeformat',
//   });