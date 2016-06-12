// Fix map for IE
if (!('map' in Array.prototype)) {
    Array.prototype.map = function (mapper, that /*opt*/) {
        var other = new Array(this.length);
        for (var i = 0, n = this.length; i < n; i++)
            if (i in this)
                other[i] = mapper.call(that, this[i], i, this);
        return other;
    };
};

var mapSVG ={};
var browser = BrowserDetect;

if (isOldBrowser()) {
    $('#old_browser_msg').show();
    $('#wtf').hide();
    $('fieldset#state').addClass('ff3');
    $('#ie8_percents').addClass('ff3');
    $('#share2').addClass('ff3');
    $('#poweredby.old_browsers').show();
}

var buckets = 11,
    colorScheme = 'rbow2',
    days = [
        //{ name: 'January', abbr: 'Jan.' },
        //{ name: 'February', abbr: 'Feb.' },
        //{ name: 'March', abbr: 'Mar.' },
        //{ name: 'April', abbr: 'Apr.' },
        //{ name: 'May', abbr: 'May.' },
        //{ name: 'Jun', abbr: 'Jun.' },
        //{ name: 'July', abbr: 'Jul.' },
        //{ name: 'August', abbr: 'Aug.'},
        //{ name: 'September', abbr: 'Sep.' },
        //{ name: 'October', abbr: 'Oct.' },
        //{ name: 'November', abbr: 'Nov.' },
        //{ name: 'December', abbr: 'Dem.' }
        { name: '2001', abbr: '2001' },
        { name: '2002', abbr: '2002' },
        { name: '2003', abbr: '2003' },
        { name: '2004', abbr: '2004' },
        { name: '2005', abbr: '2005' },
        { name: '2006', abbr: '2006' },
        { name: '2007', abbr: '2007' },
        { name: '2008', abbr: '2008'},
        { name: '2009', abbr: '2009' },
        { name: '2010', abbr: '2010' },
        { name: '2011', abbr: '2011' },
        { name: '2012', abbr: '2012' },
        { name: '2013', abbr: '2013' },
        { name: '2014', abbr: '2014' },
        { name: '2015', abbr: '2015' }
    ],
    types = {
        all: 'All',
        pc: 'Computer',
        mob: 'Mobile'
    },
    hours = ['topic1', 'topic2', 'topic3', 'topic4', 'topic5', 'topic6', 'topic7', 'topic8', 'topic9', 'topic10', 'topic11', 'topic12', 'topic13', 'topic14', 'topic15', 'topic16', 'topic17', 'topic18', 'topic19', 'topic20'],
    stateAbbrs = ['all', 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY'],
    states = {};
var data;
//
//if (isOldBrowser() === false) {
//    createMap();
//}
addStateButtons();

d3.select('#vis').classed(colorScheme, true);

d3.json('../data/output/year_topic_2D_2.json', function(json) {

    data = json;

    createTiles();
    reColorTiles('all', 'pc');

    if (isOldBrowser() === false) {
        drawMobilePie('all');
    }

    /* ************************** */

    // State map click events
    d3.selectAll('#map path.state').on('click', function() {
        var $sel = d3.select('path.state.sel'),
            prevState, currState;

        if ($sel.empty()) {
            prevState = '';
        } else {
            prevState = $sel.attr('id');
        }

        currState = d3.select(this).attr('id');

        if (prevState !== currState) {
            var type = d3.select('#type label.sel span').attr('class');
            reColorTiles(currState, type);
            drawMobilePie(currState);
        }

        d3.selectAll('#map path.state').classed('sel', false);
        d3.select(this).classed('sel', true);
        d3.select('#show_all_states').classed('sel', false);
        d3.select('#wtf h2').html(states[currState].name);
        d3.select('fieldset#state label.sel').classed('sel', false);
        d3.select('fieldset#state label[for="state_' + currState + '"]').classed('sel', true);
    });

    /* ************************** */

    // All, PC, Mobile control event listener
    $('input[name="type"]').change(function() {

        var type = $(this).val(),
            $sel = d3.select('#map path.state.sel');

        d3.selectAll('fieldset#type label').classed('sel', false);
        d3.select('label[for="type_' + type + '"]').classed('sel', true);

        if ($sel.empty()) {
            var state = 'all';
        } else {
            var state = $sel.attr('id');
        }

        reColorTiles(state, type);
        d3.select('#pc2mob').attr('class', type);

        var type = types[selectedType()];
        d3.select('#wtf .subtitle').html(type  + ' traffic daily');
    });

    /* ************************** */

    // All States click
    $('label[for="state_all"]').click(function() {

        d3.selectAll('fieldset#state label').classed('sel', false);
        $(this).addClass('sel');
        var type = d3.select('input[name="type"]').property('value');

        d3.selectAll('#map path.state').classed('sel', false);

        reColorTiles('all', type);
        drawMobilePie('all');

        d3.select('#wtf h2').html('All States');
    });

    /* ************************** */

    // Text States list event listener
    $('input[name="state"]').change(function() {

        var state = $(this).val(),
            type = d3.select('input[name="type"]').property('value');

        d3.selectAll('fieldset#state label').classed('sel', false);
        d3.select('label[for="state_' + state + '"]').classed('sel', true);

        reColorTiles(state, type);
        updateIE8percents(state);
    });

    /* ************************** */

    // tiles mouseover events
    $('#tiles td').hover(function() {

        $(this).addClass('sel');

        var tmp = $(this).attr('id').split('d').join('').split('h'),
            day = parseInt(tmp[0]),
            hour = parseInt(tmp[1]);

        var $sel = d3.select('#map path.state.sel');

        if ($sel.empty()) {
            var state = 'all';
        } else {
            var state = $sel.attr('id');
        }

        var view = 'all';

        if (isOldBrowser() === false) {
            drawHourlyChart(state, day);
            selectHourlyChartBar(hour);
        }

        var type = types[selectedType()];
        d3.select('#wtf .subtitle').html(type  + ' traffic on ' + days[day].name + 's');

    }, function() {

        $(this).removeClass('sel');

        var $sel = d3.select('#map path.state.sel');

        if ($sel.empty()) {
            var state = 'all';
        } else {
            var state = $sel.attr('id');
        }
        if (isOldBrowser() === false) {
            drawHourlyChart(state, 3);
        }
        var type = types[selectedType()];
        d3.select('#wtf .subtitle').html(type  + ' traffic daily');
    });
});

/* ************************** */

function isOldBrowser() {

    var result = false;
    if (browser.browser === 'Explorer' && browser.version < 9) {
        result = true;
    } else if (browser.browser === 'Firefox' && browser.version < 4) {
        result = true;
    }

    //console.log(result);

    return result;
}


/* ************************** */

function selectedType() {

    //return d3.select('input[name="type"]:checked').property('value'); // IE8 doesn't like this
    return $('input[name="type"]:checked').val();
}

/* ************************** */

function addStateButtons() {

    for (var i = 1; i < stateAbbrs.length; i++) {
        var abbr = stateAbbrs[i];
        var html = '<input type="radio" id="state_' + abbr + '" name="state" value="' + abbr + '"/><label for="state_' + abbr + '"><span class="' + abbr + '">' + abbr + '</span></label>';

        $('fieldset#state').append(html);
    }
}

/* ************************** */

function getCalcs(state, view) {

    var min = 1,
        max = -1;

    // calculate min + max
    for (var d = 0; d < data[state].views.length; d++) {
        for (var h = 0; h < data[state].views[d].length; h++) {

            if (view === 'all') {
                var tot = data[state].views[d][h].pc + data[state].views[d][h].mob;
            } else {
                var tot = data[state].views[d][h][view];
            }

            if (tot > max) {
                max = tot;
            }

            if (tot < min) {
                min = tot;
            }
        }
    }

    return {'min': min, 'max': max};
};

/* ************************** */

function reColorTiles(state, view) {

    var calcs = getCalcs(state, view),
        range = [];

    for (var i = 1; i <= buckets; i++) {
        range.push(i);
    }

    var bucket = d3.scale.quantize().domain([0, calcs.max > 0 ? calcs.max : 1]).range(range),
        side = d3.select('#tiles').attr('class');


    if (side === 'front') {
        side = 'back';
    } else {
        side = 'front';
    }

    for (var d = 0; d < data[state].views.length; d++) {
        for (var h = 0; h < data[state].views[d].length; h++) {

            var sel = '#d' + d + 'h' + h + ' .tile .' + side,
                val = data[state].views[d][h].pc + data[state].views[d][h].mob;

            if (view !== 'all') {
                val = data[state].views[d][h][view];
            }

            // erase all previous bucket designations on this cell
            for (var i = 1; i <= buckets; i++) {
                var cls = 'q' + i + '-' + buckets;
                d3.select(sel).classed(cls , false);
            }

            // set new bucket designation for this cell
            var cls = 'q' + (val > 0 ? bucket(val) : 0) + '-' + buckets;
            d3.select(sel).classed(cls, true);
        }
    }
    flipTiles();
    if (isOldBrowser() === false) {
        drawHourlyChart(state, 3);
    }
}

/* ************************** */

function flipTiles() {

    var oldSide = d3.select('#tiles').attr('class'),
        newSide = '';

    if (oldSide == 'front') {
        newSide = 'back';
    } else {
        newSide = 'front';
    }

    var flipper = function(h, d, side) {
        return function() {
            var sel = '#d' + d + 'h' + h + ' .tile',
                rotateY = 'rotateY(180deg)';

            if (side === 'back') {
                rotateY = 'rotateY(0deg)';
            }
            if (browser.browser === 'Safari' || browser.browser === 'Chrome') {
                d3.select(sel).style('-webkit-transform', rotateY);
            } else {
                d3.select(sel).select('.' + oldSide).classed('hidden', true);
                d3.select(sel).select('.' + newSide).classed('hidden', false);
            }

        };
    };

    for (var h = 0; h < hours.length; h++) {
        for (var d = 0; d < days.length; d++) {
            var side = d3.select('#tiles').attr('class');
            setTimeout(flipper(h, d, side), (h * 20) + (d * 20) + (Math.random() * 100));
        }
    }
    d3.select('#tiles').attr('class', newSide);
}

/* ************************** */

function drawHourlyChart(state, day) {

    d3.selectAll('#hourly_values svg').remove();

    var w = 300,
        h = 150;

    var weeklyData = data[state].views[day],
        view = d3.select('#type label.sel span').attr('class');


    var y = d3.scale.linear()
        .domain([0, d3.max(weeklyData, function(d) { return (view === 'all') ? d.pc + d.mob : d[view] })])
        .range([0, h]);


    var chart = d3.select('#hourly_values .svg')
        .append('svg:svg')
        .attr('class', 'chart')
        .attr('width', 300)
        .attr('height', 170);

    var rect = chart.selectAll('rect'),
        text = chart.selectAll('text');

    rect.data(weeklyData)
        .enter()
        .append('svg:rect')
        .attr('x', function(d, i) { return i * 12; })
        .attr('y', function(d) { return (view === 'all') ? h - y(d.pc + d.mob) : h - y(d[view]) })
        .attr('height', function(d) { return (view === 'all') ? y(d.pc + d.mob) : y(d[view]) })
        .attr('width', 10)
        .attr('class', function(d, i) { return 'hr' + i});

    text.data(hours)
        .enter()
        .append('svg:text')
        .attr('class', function(d, i) { return (i % 3) ? 'hidden hr' + i : 'visible hr' + i })
        .attr("x", function(d, i) { return i * 12 })
        .attr("y", 166)
        .attr("text-anchor", 'left')
        .text(String);
}

/* ************************** */

function drawMobilePie(state) {

    var w = 150,
        h = 150,
        r = Math.min(w, h) / 2,
        pieData = [1, data[state].pc2mob],
        pie = d3.layout.pie(),
        arc = d3.svg.arc().innerRadius(0).outerRadius(r),
        type = selectedType();

    d3.select('#pc2mob').attr('class', type);
    d3.selectAll('#pc2mob svg').remove();

    var chart = d3.select("#pc2mob .svg").append('svg:svg')
        .data([pieData])
        .attr("width", w)
        .attr("height", h);

    var arcs = chart.selectAll('g')
        .data(pie)
        .enter().append('svg:g')
        .attr("transform", "translate(" + r + "," + r + ")");

    arcs.append('svg:path')
        .attr('d', arc)
        .attr('class', function(d, i) { return i === 0 ? 'mob' : 'pc' });

    var rawMobPercent = 100 / (data[state].pc2mob + 1);

    if (rawMobPercent < 1) {
        var mobPercent = '< 1',
            pcPercent = '> 99';
    } else {
        var mobPercent = Math.round(rawMobPercent),
            pcPercent = 100 - mobPercent;
    }

    d3.select('#pc2mob .pc span').html(pcPercent + '%');
    d3.select('#pc2mob .mob span').html(mobPercent + '%');

    var html = d3.select('#pc2mob ul').html();
    d3.select('#ie8_percents').html(html);
}

/* ************************** */

function updateIE8percents(state) {

    var rawMobPercent = 100 / (data[state].pc2mob + 1);

    if (rawMobPercent < 1) {
        var mobPercent = '< 1',
            pcPercent = '> 99';
    } else {
        var mobPercent = Math.round(rawMobPercent),
            pcPercent = 100 - mobPercent;
    }

    d3.select('#pc2mob .pc span').html(pcPercent + '%');
    d3.select('#pc2mob .mob span').html(mobPercent + '%');

    var html = d3.select('#pc2mob ul').html();
    d3.select('#ie8_percents').html(html);
}




/* ************************** */

function createTiles() {

    var html = '<table id="tiles" class="front">';

    html += '<tr><th><div>&nbsp;</div></th>';

    for (var h = 0; h < hours.length; h++) {
        html += '<th class="h' + h + '">' + hours[h] + '</th>';
    }

    html += '</tr>';

    for (var d = 0; d < days.length; d++) {
        html += '<tr class="d' + d + '">';
        html += '<th>' + days[d].abbr + '</th>';
        for (var h = 0; h < hours.length; h++) {
            html += '<td id="d' + d + 'h' + h + '" class="d' + d + ' h' + h + '"><div class="tile"><div class="face front"></div><div class="face back"></div></div></td>';
        }
        html += '</tr>';
    }

    html += '</table>';
    d3.select('#vis').html(html);
}

/* ************************** */

function selectHourlyChartBar(hour) {

    d3.selectAll('#hourly_values .chart rect').classed('sel', false);
    d3.selectAll('#hourly_values .chart rect.hr' + hour).classed('sel', true);

    d3.selectAll('#hourly_values .chart text').classed('hidden', true);
    d3.selectAll('#hourly_values .chart text.hr' + hour).classed('hidden', false);

};

/* ************************** */

//function createMap() {
//    var svg = d3.select("#map").append('svg:svg')
//        .attr('width', 320)
//        .attr('height', 202);
//
//    var g = svg.append('svg:g')
//        .attr('transform', 'scale(0.5) translate(-27, -134)');
//
//    for (s = 0; s < mapSVG.states.length; s++ ) {
//        var state = mapSVG.states[s];
//
//        var path = g.append('svg:path')
//            .attr('id', state)
//            .attr('class', 'state')
//            .attr('d', mapSVG[state]);
//    }
//}