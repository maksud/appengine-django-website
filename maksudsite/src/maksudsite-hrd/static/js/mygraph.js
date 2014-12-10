function Graph(el, weight, height) {

    // set up the D3 visualisation in the specified element
    var w = weight,
        h = height;

    // Add and remove elements on the graph object
    this.addNode = function(id, group) {
        nodes.push({
            "id": id,
            "group": group
        });
        update();
    };

    this.removeNode = function(id) {
        var i = 0;
        var n = findNode(id);
        while (i < links.length) {
            if ((links[i]['source'] == n) || (links[i]['target'] == n)) {
                links.splice(i, 1);
            } else i++;
        }
        nodes.splice(findNodeIndex(id), 1);
        update();
    };

    this.removeLink = function(source, target) {
        for (var i = 0; i < links.length; i++) {
            if (links[i].source.id == source && links[i].target.id == target) {
                links.splice(i, 1);
                break;
            }
        }
        update();
    };

    this.removeAllLinks = function() {
        links.splice(0, links.length);
        update();
    };

    this.removeAllNodes = function() {
        nodes.splice(0, nodes.length);
        update();
    };

    this.addLink = function(source, target, value) {
        links.push({
            "source": findNode(source),
            "target": findNode(target),
            "value": value
        });
        update();
    };

    var findNode = function(id) {
        for (var i in nodes) {
            if (nodes[i]["id"] === id) return nodes[i];
        };
    };

    var findNodeIndex = function(id) {
        for (var i = 0; i < nodes.length; i++) {
            if (nodes[i].id == id) {
                return i;
            }
        };
    };

    var vis = d3.select(el)
        .append("svg:svg")
        .attr("width", w)
        .attr("height", h)
        .attr("id", "svg")
        .attr("pointer-events", "all")
        .attr("viewBox", "0 0 " + w + " " + h)
        .attr("perserveAspectRatio", "xMinYMid")
        .append('svg:g');

    var force = d3.layout.force();

    var color = d3.scale.category20();

    var nodes = force.nodes(),
        links = force.links();

    var update = function() {

        var link = vis.selectAll("line")
            .data(links, function(d) {
                return d.source.id + "-" + d.target.id;
            });

        link.enter()
            .insert("line", ":first-child")
            // .append("line")
            .attr("id", function(d) {
                return d.source.id + "-" + d.target.id;
            })
            .attr("class", "link");
        // link.append("title").text(function(d){
        //     	return d.value;
        // });
        link.exit().remove();

        var node = vis.selectAll("circle")
            .data(nodes, function(d) {
                return d.id;
            });

        var nodeEnter = node.enter()
            // .append("g")
            // nodeEnter
            .append("svg:circle")
            .attr("class", "node")
            // .attr("r", 5)
            .attr("id", function(d) {
                return "Node;" + d.id;
            })
            // .on("mouseover", function(d) {
            //     var g = d3.select(this); // The node
            //     // The class is used to remove the additional text later
            //     var info = g.append('text')
            //         .classed('info', true)
            //         .attr('x', 20)
            //         .attr('y', 10)
            //         .text('More info');
            // })
            // .on("mouseout", function() {
            //     // Remove the info text on mouse out.
            //     d3.select(this).select('text.info').remove();
            // })
            // .attr("class","nodeStrokeClass")
            .call(force.drag);


        //	    ndoeEnter.append("svg:text")
        //	    .attr("class","textClass")
        //	    .text( function(d){return d.id;}) ;

        node.exit().remove();

        force.on("tick", function() {
            node.attr("transform", function(d) {
                return "translate(" + d.x + "," + d.y + ")";
            });

            link.attr("x1", function(d) {
                    return d.source.x;
                })
                .attr("y1", function(d) {
                    return d.source.y;
                })
                .attr("x2", function(d) {
                    return d.target.x;
                })
                .attr("y2", function(d) {
                    return d.target.y;
                });
        });

        // Restart the force layout.
        force
        // .gravity(.05)
        //.distance(50)
        //.linkDistance( 50 )
            .size([w, h])
            .start();

        vis.selectAll("circle.node")
            .attr('r', function(d) {
                return Math.max(3, 2 + Math.sqrt(d.weight));
            })
            .style("fill", function(d) {
                return color(d.weight);
            });
    };


    // Make it all go
    update();
}