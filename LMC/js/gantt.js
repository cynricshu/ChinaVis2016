/**
 * Created by yichli on 6/12/16.
 */

var init = [
    {
        "count": 259224,
        "endDate": "2015-06-06 15:15:57",
        "startDate": "2001-06-30 01:38:19",
        "status": 5.057459957411351,
        "taskName": "topic0"
    },
    {
        "count": 148470,
        "endDate": "2016-01-01 22:13:21",
        "startDate": "2005-10-14 22:59:19",
        "status": 5.072944029096788,
        "taskName": "topic1"
    },
    {
        "count": 131854,
        "endDate": "2015-06-06 12:15:52",
        "startDate": "2005-10-19 18:06:26",
        "status": 5.0366314256677835,
        "taskName": "topic2"
    },
    {
        "count": 137539,
        "endDate": "2015-06-10 06:18:18",
        "startDate": "2005-10-24 15:26:20",
        "status": 5.063109372614313,
        "taskName": "topic3"
    },
    {
        "count": 134787,
        "endDate": "2015-06-06 14:01:50",
        "startDate": "2005-10-19 17:24:16",
        "status": 5.061467352192719,
        "taskName": "topic4"
    },
    {
        "count": 112241,
        "endDate": "2015-06-10 06:18:18",
        "startDate": "2003-12-02 08:04:59",
        "status": 5.0865102769932555,
        "taskName": "topic5"
    },
    {
        "count": 237655,
        "endDate": "2015-06-06 01:43:29",
        "startDate": "2005-10-17 15:32:48",
        "status": 5.045317792598515,
        "taskName": "topic6"
    },
    {
        "count": 217013,
        "endDate": "2015-06-06 14:42:57",
        "startDate": "2004-01-15 07:41:00",
        "status": 5.0385230377903625,
        "taskName": "topic7"
    },
    {
        "count": 117434,
        "endDate": "2015-06-06 14:08:35",
        "startDate": "2005-10-20 16:34:06",
        "status": 5.053774886319124,
        "taskName": "topic8"
    },
    {
        "count": 131206,
        "endDate": "2015-06-06 01:30:49",
        "startDate": "2002-01-01 12:34:50",
        "status": 5.0525890584272055,
        "taskName": "topic9"
    },
    {
        "count": 127191,
        "endDate": "2016-01-31 14:34:14",
        "startDate": "2002-02-14 13:57:45",
        "status": 5.0606174965209805,
        "taskName": "topic10"
    },
    {
        "count": 65829,
        "endDate": "2015-06-06 13:08:54",
        "startDate": "2005-10-14 15:05:35",
        "status": 5.046635981102554,
        "taskName": "topic11"
    },
    {
        "count": 111851,
        "endDate": "2015-06-27 19:42:17",
        "startDate": "2001-06-29 19:31:43",
        "status": 5.049083155269063,
        "taskName": "topic12"
    },
    {
        "count": 307400,
        "endDate": "2015-06-06 16:28:10",
        "startDate": "2002-01-14 08:08:40",
        "status": 5.073536109303839,
        "taskName": "topic13"
    },
    {
        "count": 64451,
        "endDate": "2015-06-06 14:16:14",
        "startDate": "2001-01-01 16:37:22",
        "status": 5.061131712463732,
        "taskName": "topic14"
    },
    {
        "count": 94246,
        "endDate": "2015-06-06 14:00:04",
        "startDate": "2005-10-20 23:13:33",
        "status": 5.021592428325871,
        "taskName": "topic15"
    },
    {
        "count": 79419,
        "endDate": "2015-06-06 12:32:51",
        "startDate": "2005-11-07 21:21:38",
        "status": 5.068749291731198,
        "taskName": "topic16"
    },
    {
        "count": 98270,
        "endDate": "2015-06-06 13:57:50",
        "startDate": "2003-04-26 09:04:23",
        "status": 5.0988602828940675,
        "taskName": "topic17"
    },
    {
        "count": 72238,
        "endDate": "2015-06-06 15:40:27",
        "startDate": "2005-10-25 22:55:22",
        "status": 4.952448849635926,
        "taskName": "topic18"
    },
    {
        "count": 62855,
        "endDate": "2015-06-06 17:13:10",
        "startDate": "2005-11-02 18:49:15",
        "status": 5.079548166414765,
        "taskName": "topic19"
    }
];

    var color = d3.scale.category20c();
    var tasks = [];
    var taskNames = [];
    $.each(init,function(i,item){
        taskNames.push(item['taskName']);
        var temp = {};
        temp.startDate = new Date(item['startDate']);
        temp.endDate = new Date(item['endDate']);
        temp.taskName = item['taskName'];
        temp.status = color(item['status']);
        console.log(temp.status);
        tasks.push(temp);
    });



//var tasks = [
//    {"startDate":new Date("Sun Dec 09 01:36:45 EST 2012"),"endDate":new Date("Sun Dec 09 02:36:45 EST 2012"),"taskName":"E Job","status":"RUNNING"},
//    {"startDate":new Date("Sun Dec 09 04:56:32 EST 2012"),"endDate":new Date("Sun Dec 09 06:35:47 EST 2012"),"taskName":"A Job","status":"RUNNING"},
//    {"startDate":new Date("Sun Dec 09 06:29:53 EST 2012"),"endDate":new Date("Sun Dec 09 06:34:04 EST 2012"),"taskName":"D Job","status":"RUNNING"},
//    {"startDate":new Date("Sun Dec 09 05:35:21 EST 2012"),"endDate":new Date("Sun Dec 09 06:21:22 EST 2012"),"taskName":"P Job","status":"RUNNING"},
//    {"startDate":new Date("Sun Dec 09 05:00:06 EST 2012"),"endDate":new Date("Sun Dec 09 05:05:07 EST 2012"),"taskName":"D Job","status":"RUNNING"},
//    {"startDate":new Date("Sun Dec 09 03:46:59 EST 2012"),"endDate":new Date("Sun Dec 09 04:54:19 EST 2012"),"taskName":"P Job","status":"RUNNING"},
//    {"startDate":new Date("Sun Dec 09 04:02:45 EST 2012"),"endDate":new Date("Sun Dec 09 04:48:56 EST 2012"),"taskName":"N Job","status":"RUNNING"},
//    {"startDate":new Date("Sun Dec 09 03:27:35 EST 2012"),"endDate":new Date("Sun Dec 09 03:58:43 EST 2012"),"taskName":"E Job","status":"SUCCEEDED"},
//    {"startDate":new Date("Sun Dec 09 01:40:11 EST 2012"),"endDate":new Date("Sun Dec 09 03:26:35 EST 2012"),"taskName":"A Job","status":"SUCCEEDED"},
//    {"startDate":new Date("Sun Dec 09 03:00:03 EST 2012"),"endDate":new Date("Sun Dec 09 03:09:51 EST 2012"),"taskName":"D Job","status":"SUCCEEDED"},
//    {"startDate":new Date("Sun Dec 09 01:21:00 EST 2012"),"endDate":new Date("Sun Dec 09 02:51:42 EST 2012"),"taskName":"P Job","status":"SUCCEEDED"},
//    {"startDate":new Date("Sun Dec 09 01:08:42 EST 2012"),"endDate":new Date("Sun Dec 09 01:33:42 EST 2012"),"taskName":"N Job","status":"FAILED"},
//    {"startDate":new Date("Sun Dec 09 00:27:15 EST 2012"),"endDate":new Date("Sun Dec 09 00:54:56 EST 2012"),"taskName":"E Job","status":"SUCCEEDED"},
//    {"startDate":new Date("Sun Dec 09 00:29:48 EST 2012"),"endDate":new Date("Sun Dec 09 00:44:50 EST 2012"),"taskName":"D Job","status":"SUCCEEDED"},
//    {"startDate":new Date("Sun Dec 09 07:39:21 EST 2012"),"endDate":new Date("Sun Dec 09 07:43:22 EST 2012"),"taskName":"P Job","status":"RUNNING"},
//    {"startDate":new Date("Sun Dec 10 07:00:06 EST 2012"),"endDate":new Date("Sun Dec 10 07:05:07 EST 2013"),"taskName":"D Job","status":"RUNNING"},
//    {"startDate":new Date("Sun Dec 09 08:46:59 EST 2012"),"endDate":new Date("Sun Dec 09 09:54:19 EST 2012"),"taskName":"P Job","status":"RUNNING"},
//    {"startDate":new Date("Sun Dec 09 09:02:45 EST 2012"),"endDate":new Date("Sun Dec 09 09:48:56 EST 2012"),"taskName":"N Job","status":"RUNNING"},
//    {"startDate":new Date("Sun Dec 09 08:27:35 EST 2012"),"endDate":new Date("Sun Dec 09 08:58:43 EST 2012"),"taskName":"E Job","status":"SUCCEEDED"},
//    {"startDate":new Date("Sun Dec 09 08:40:11 EST 2012"),"endDate":new Date("Sun Dec 09 08:46:35 EST 2012"),"taskName":"A Job","status":"SUCCEEDED"},
//    {"startDate":new Date("Sun Dec 09 08:00:03 EST 2012"),"endDate":new Date("Sun Dec 09 08:09:51 EST 2012"),"taskName":"D Job","status":"SUCCEEDED"},
//    {"startDate":new Date("Sun Dec 09 10:21:00 EST 2012"),"endDate":new Date("Sun Dec 09 10:51:42 EST 2012"),"taskName":"P Job","status":"SUCCEEDED"},
//    {"startDate":new Date("Sun Dec 09 11:08:42 EST 2012"),"endDate":new Date("Sun Dec 09 11:33:42 EST 2012"),"taskName":"N Job","status":"FAILED"},
//    {"startDate":new Date("Sun Dec 09 12:27:15 EST 2012"),"endDate":new Date("Sun Dec 09 12:54:56 EST 2012"),"taskName":"E Job","status":"SUCCEEDED"},
//    {"startDate":new Date("Sat Dec 08 23:12:24 EST 2012"),"endDate":new Date("Sun Dec 09 00:26:13 EST 2012"),"taskName":"A Job","status":"KILLED"}];

var taskStatus = {
    "#3182bd":"topic1",
    "#6baed6":"topic2",
    "#9ecae1":"topic3",
    "#c6dbef":"topic4",
    "#e6550d":"topic5",
    "#fd8d3c":"topic6",
    "#fdae6b":"topic7",
    "#fdd0a2":"topic8",
    "#31a354":"topic9",
    "#74c476":"topic10",
    "#a1d99b":"topic11",
    "#c7e9c0":"topic12",
    "#756bb1":"topic13",
    "#9e9ac8":"topic14",
    "#bcbddc":"topic15",
    "#dadaeb":"topic16",
    "#636363":"topic17",
    "#969696":"topic18",
    "#bdbdbd":"topic19"
};

//var taskNames = [ "D Job", "P Job", "E Job", "A Job", "N Job" ];

tasks.sort(function(a, b) {
    return a.endDate - b.endDate;
});
var maxDate = tasks[tasks.length - 1].endDate;
tasks.sort(function(a, b) {
    return a.startDate - b.startDate;
});
var minDate = tasks[0].startDate;

var format = "%H:%M";

var gantt = d3.gantt().taskTypes(taskNames).taskStatus(taskStatus).tickFormat(format);
gantt(tasks);