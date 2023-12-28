const ctx = document.getElementById("myChart").getContext("2d");

const labels = [
    '2014',
    '2015',
    '2016',
    '2017',
    '2018',
    '2019',
    '2020',
    '2021',
    '2022',
    '2023',
];

const data = {
    labels, 
    datasets: [{
        data: [221, 100, 50, 545, 533, 66, 586, 144, 659, 322],
        label: "Sales",
    },
],
};

const config = {
    type:'bar',
    data: data,
    option: {
        responsive:true,
    },
};

const myChart = new Chart(ctx, config);

