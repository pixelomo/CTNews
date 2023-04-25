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

    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');

    sidebarToggle.addEventListener('click', () => {
        sidebar.style.transform = sidebar.style.transform === 'translateX(calc(-100% + 30px))' ? 'translateX(0)' : 'translateX(calc(-100% + 30px))';
        // sidebarToggle.style.transform = sidebar.style.transform === 'translateX(-100%)' ? 'translateX(100%)' : 'translateX(0)';
        sidebarToggle.innerHTML = sidebar.style.transform === 'translateX(calc(-100% + 30px))' ? '<svg width="800px" height="800px" viewBox="0 0 24 24" mirror-in-rtl="true"><path fill="#ffffff" d="M10.25 22.987l7.99-9c.51-.57.76-1.28.76-1.99s-.25-1.42-.74-1.98c-.01 0-.01-.01-.01-.01l-.02-.02-7.98-8.98c-1.1-1.24-3.002-1.35-4.242-.25-1.24 1.1-1.35 3-.25 4.23l6.23 7.01-6.23 7.01c-1.1 1.24-.99 3.13.25 4.24 1.24 1.1 3.13.98 4.24-.26z"/></svg>' : '<svg width="800" height="800" viewBox="0 0 24 24" mirror-in-rtl="true"><path fill="#ffffff" d="M13.75 22.987l-7.99-9c-.51-.57-.76-1.28-.76-1.99s.25-1.42.74-1.98c.01 0 .01-.01.01-.01l.02-.02 7.98-8.98c1.1-1.24 3.002-1.35 4.242-.25 1.24 1.1 1.35 3 .25 4.23l-6.23 7.01 6.23 7.01c1.1 1.24.99 3.13-.25 4.24-1.24 1.1-3.13.98-4.24-.26z"/></svg>';
    });

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

    const tabButtons = document.querySelectorAll('.tab-button');
    const tabs = document.querySelectorAll('.tab');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const target = button.getAttribute('data-target');
            // Update button active state
            tabButtons.forEach(btn => {
                btn.classList.toggle('active', btn.getAttribute('data-target') === target);
            });
            // Show/hide tabs
            tabs.forEach(tab => {
                tab.style.display = tab.getAttribute('id') === target ? 'block' : 'none';
            });
        });
    });


});