datasets = { "Q1": { label: "Q1", data: [[0,1], [2,1], [3,4]]}, "Q2": { label: "Q2", data: [[0,1], [2,1], [3,4]]} };
// Data is of the form of [[Day-#, value], [Day-#, value], ... ]
// Value ranges from 0 to X (there's no support for negative values)
function plot_graph (datasets) {
    // Hard-code color indices to prevent them from shifting
    var i = 0;
    $.each(datasets, function(key, val) {
        val.color = i;
        ++i;
    });

    // Show textboxes 
    var choice_container = $("#choices");
    $.each(datasets, function(key, val) {
        choice_container.append('<br/><input type="checkbox" name="' + key +
                               '" checked="checked" id="id' + key + '">' +
                               '<label for="id' + key + '">'
                                + val.label + '</label>');
    });
    choice_container.find("input").click(plot_choices);

    // Finally, plot the graph based on the selected boxes
    function plot_choices() {
        var data = [];

        choice_container.find("input:checked").each(function () {
            var key = $(this).attr("name");
            if (key && datasets[key])
                data.push(datasets[key]);
        });

        if (data.length > 0)
            $.plot($("#placeholder"), data, {
                yaxis: { min: 0 },
                xaxis: { tickDecimals: 0 }
            });
    }

    plot_choices();
};

function set_explanation(text) {
    var explanation_container = $("#explanation");
    explanation_container.html(text);
};
