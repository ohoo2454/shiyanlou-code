// 保存定时时间
var time = 0;

// 设置是否暂停标志，true表示暂停
var pause = true;

// 设置定时函数
var set_timer;

// 保存大DIV当前装的小DIV的编号
var d = new Array(10);

// 保存大DIV编号的可移动位置编号
var d_direct = new Array(
    [0],  // 为了逻辑更简单，第一个元素我们不用，我们从下标1开始使用
    [2, 4],  // 大DIV编号为1的DIV可以去的位置，比如第一块可以去2，4号位置
    [1, 3, 5],
    [2, 6],
    [1, 5, 7],
    [2, 4, 6, 8],
    [3, 5, 9],
    [4, 8],
    [5, 7, 9],
    [6, 8]
);

// 大DIV编号的位置
var d_posXY = new Array(
    [0],  // 同样，我们不使用第一个元素
    [0, 0],  // 第一个表示left，第二个表示top，比如第一块的位置为left: 0px, top: 0px
    [150, 0],
    [300, 0],
    [0, 150],
    [150, 150],
    [300, 150],
    [0, 300],
    [150, 300],
    [300, 300]
);

// 默认按照顺序排好，大DIV第九块没有，所以为0，我们用0表示空白块
d[1] = 1;
d[2] = 2;
d[3] = 3;
d[4] = 4;
d[5] = 5;
d[6] = 6;
d[7] = 7;
d[8] = 8;
d[9] = 0;

// 移动函数
function move(id) {
    var i = 1;
    for (i=1; i<10; i++) {
        if (d[i] == id) {
            break;
        }
    }
}

// 判断是否可移动函数，参数是大DIV的编号，不是小DIV的编号，因为小DIV编号和可以去哪没关系，小DIV是可移动的
function whereCanTo(cur_div) {
    
}

// 定时函数，每一秒执行一次
function timer() {
    
}

// 开始暂停函数
function start() {

}

// 重置函数
function reset() {
    
}

// 随机打乱方块函数，我们的思路是从第九块开始，随机生成一个数，然后他们两块对调一下
function random_d() {
    
}

// 初始化函数，页面加载的时候调用重置函数，重新开始
window.onload = function () {
    reset();
}
