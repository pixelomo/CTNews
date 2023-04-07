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
