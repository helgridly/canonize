
window.onload = function() {
    fetch("contents.json")
      .then(response => response.json())
      .then(data => {
        
        // convert mentions array to string
        data.forEach(item => {
          if (item.mentions) {
            item.mentions = item.mentions.join(", ");
          }

          if (item.tags) {
            item.tags = item.tags.join(", ");
          }
        });
  
        const table = new Tabulator("#data-table", {
          data: data,
          layout: "fitColumns",
          columns: [
            { 
              title: "Title", 
              field: "title", 
              sorter: "string",
              widthGrow: 2,
              headerFilter: "input",  // This adds the filter input to the header
              headerFilterPlaceholder: "Search titles...", // Optional placeholder text
              // format the title as an href using the path column on this row
              formatter: function(cell, formatterParams, onRendered) {
                return '<a href="' + cell.getRow().getCell("path").getValue() + '">' + cell.getValue() + '</a>';
              }
            },
            {
                title: "Tags",
                field: "tags",
                headerFilter: "list",
                headerFilterParams: {
                  values: [...new Set(data.flatMap(item => (item.tags && item.tags.split(", ")) || []))],
                  autocomplete: true,
                  filterFunc : function(term, label, value, item) {
                      if (!value) return false;
                      return value.includes(term);
                  }
                },
                headerFilterFunc: "like",
              },
            {
              title: "Mentions",
              field: "mentions",
              headerFilter: "list",
              headerFilterParams: {
                values: [...new Set(data.flatMap(item => (item.mentions && item.mentions.split(', ')) || []))],
                // autocomplete: false, clearable: true gives us what we want (a selectable dropdown), but doesn't work
                // in firefox: https://github.com/olifolkerd/tabulator/issues/3813#issuecomment-1610984347
                // because the X-to-clear isn't displayed by default; even with an about:config flag set, see the "some issues
                // still to be solved" link - this is a FF bug
                // so in the meantime we use autocomplete and make the user type
                autocomplete: true,
                filterFunc : function(term, label, value, item) {
                    if (!value) return false;
                    return value.includes(term);
                }
              },
              headerFilterFunc: "like",
            },
            { title: "Created", field: "creation_date", sorter: "datetime" },
            { title: "Updated", field: "last_updated", sorter: "datetime" },
            { title: "Path", field: "path", sorter: "string", visible: false},
            { title: "Draft", field: "draft", sorter: "boolean", visible: false },
          ]
        });
      });
  };
