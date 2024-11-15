// replaces hrefs with class "randomTag" with a random instance of an article with that tag

window.onload = function() {
    cacheBust = document.getElementById("sitetime").content;
    fetch("../../contents.json?v=" + cacheBust)
      .then(response => response.json())
      .then(data => {

        // organize the data by tag
        const tags = new Map();
        data.forEach(item => {
          if (item.tags 
              && !item.draft 
              && "/" + item.path + "/" != window.location.pathname) {
            console.log("item.path", item.path, "window.location.pathname", window.location.pathname);
            item.tags.forEach(tag => {
              tags.set(tag, tags.get(tag) || []);
              tags.get(tag).push(item);
            });
          }
        });

        const links = document.querySelectorAll(".randomTag");
            links.forEach(link => {
                const url = link.getAttribute("data-tag");
                // set the href to a random article with the same tag
                const randomArticle = tags.get(url)[Math.floor(Math.random() * tags.get(url).length)];
                link.setAttribute("href", "../../" + randomArticle.path);
            });
      });
    };
