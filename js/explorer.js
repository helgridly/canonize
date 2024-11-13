

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
          initialSort: [
            { column: "last_updated", dir: "desc" }],
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
                cell_text = cell.getValue();
                path = cell.getRow().getCell("path").getValue()
                if(cell.getRow().getCell("draft").getValue()) {
                    cell_text = "📝" + cell_text
                }
                
                return '<a href="' + path + '">' + cell_text + '</a>';
              }
            },
            {
                title: "Tags",
                field: "tags",
                headerFilter: "list",
                headerFilterPlaceholder: "choose tag",
                headerFilterParams: {
                  values: [...new Set(data.flatMap(item => (item.tags && item.tags.split(", ")) || []))].sort(),
                  autocomplete: false, clearable: true,
                  //autocomplete: true,
                  //filterFunc : function(term, label, value, item) {
                  //    if (!value) return false;
                  //    return value.includes(term);
                  //}
                },
                headerFilterFunc: "like",
              },
            {
              title: "Mentions",
              field: "mentions",
              headerFilter: "list",
              headerFilterPlaceholder: "choose user",
              headerFilterParams: {
                values: [...new Set(data.flatMap(item => (item.mentions && item.mentions.split(', ')) || []))].sort((a, b) => a.toLowerCase().localeCompare(b.toLowerCase())),
                autocomplete: false, clearable: true, //gives us what we want (a selectable dropdown), but doesn't work
                // in firefox: https://github.com/olifolkerd/tabulator/issues/3813#issuecomment-1610984347
                // because the X-to-clear isn't displayed by default; even with an about:config flag set, see the "some issues
                // still to be solved" link - this is a FF bug
                
                // so in the meantime we use autocomplete and make the user type; uncomment below to do that
                //autocomplete: true,
                //filterFunc : function(term, label, value, item) {
                //    if (!value) return false;
                //    return value.includes(term);
                //}
              },
              headerFilterFunc: "like",
            },

            { title: "Updated", field: "last_updated", sorter: "date",
              sorterParams: { format: "iso", alignEmptyValues:"top", },
              formatter: "datetime", formatterParams: { inputFormat: "iso", outputFormat: "d MMM yyyy HH:mm" }
            },
            { title: "Created", field: "creation_date", sorter: "date",
              sorterParams: { format: "iso", alignEmptyValues:"top", },
              formatter: "datetime", formatterParams: { inputFormat: "iso", outputFormat: "d MMM yyyy HH:mm" }
            },

            { title: "Path", field: "path", sorter: "string", visible: false},
            { title: "Draft", field: "draft", sorter: "boolean", visible: false },
          ]
        });

        table.on("tableBuilt", function() {
            // initialFilter doesn't work for some reason
            table.setFilter("draft", "=", false)    
        })

        // get the show-drafts checkbox
        const showDraftsCheckbox = document.getElementById("show-drafts");
        //set its onchange
        showDraftsCheckbox.addEventListener("change", function() {
          if( this.checked ) {
            table.removeFilter("draft", "=", false)
          } else {
            // add tabulator boolean filter that will only show non-drafts
            table.setFilter("draft", "=", false)
          }
        })

      });
  };
