$(document).ready(function () {
    tinymce.init({
        selector: "#translation-editor",
        height: '100vh',
        plugins: 'anchor autolink code charmap codesample image link lists media searchreplace table wordcount',
        toolbar: 'undo redo | fontfamily fontsize | bold italic underline strikethrough | link image media table | align lineheight | numlist bullist indent outdent | charmap | removeformat | code',
        content_style: 'img { max-width: 100% !important; } .mce-content-body { padding-bottom: 6rem !important; }',
        init_instance_callback: function (editor) {
            syncTinyMCEScroll(editor);
        },
    });

    function loadArticles() {
        // Use the appropriate route based on the environment
        var articlesRoute = location.hostname === "localhost" || location.hostname === "127.0.0.1"
            ? "/api/get_dummy_data"
            : "/api/get_all_articles";

        $.getJSON(articlesRoute, function (data) {
            if (!Array.isArray(data)) {
                data = [data];
            }

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

    function syncTinyMCEScroll(editor) {
        var syncScrolling = false;
        var originalScrollContainer = $(".scroll-container").not(".tox-edit-area__iframe").get(0);
        var iframeWindow = editor.getWin();
        var iframeBody = editor.getBody();

        iframeWindow.addEventListener("scroll", function () {
          if (!syncScrolling) {
            syncScrolling = true;
            originalScrollContainer.scrollTop = iframeWindow.pageYOffset;
            syncScrolling = false;
          }
        });

        $(originalScrollContainer).scroll(function () {
          if (!syncScrolling) {
            syncScrolling = true;
            iframeWindow.scrollTo(0, originalScrollContainer.scrollTop);
            syncScrolling = false;
          }
        });

        // Trigger the scroll synchronization after the content is loaded into the TinyMCE editor
        editor.on('LoadContent', function () {
          setTimeout(function () {
            originalScrollContainer.scrollTop = iframeBody.scrollTop;
          }, 100);
        });
    }


});