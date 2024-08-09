var pxInd;
var stInd;
var dispW;
var dispH;
var xhReq;
var dispX;
var rqPrf;
var rqMsg;
function byteToStr(v) {
    return String.fromCharCode((v & 15) + 97, (v >> 4 & 15) + 97);
}
function wordToStr(v) {
    return byteToStr(v & 255) + byteToStr(v >> 8 & 255);
}
function u_send(cmd, next) {
    xhReq.open('POST', rqPrf + cmd, true);
    xhReq.send('');
    if (next) {
        stInd++;
    }
    return 0;
}
function u_next() {
    lnInd = 0;
    pxInd = 0;
    u_send('NEXT_', true);
}
function u_done() {
    setInn('logTag', 'Complete!');
    return u_send('SHOW_', true);
}
function u_show(a, k1, k2) {
    var substring = '' + (k1 + k2 * pxInd / a.length);
    if (substring.length > 5) {
        substring = substring.substring(0, 5);
    }
    setInn('logTag', 'Progress: ' + substring + '%');
    return u_send(rqMsg + wordToStr(rqMsg.length) + 'LOAD_', pxInd >= a.length);
}
function u_data(a, c, k1, k2) {
    rqMsg = '';
    if (c == -1) {
        while (pxInd < a.length && rqMsg.length < 1000) {
            var _num = 0;
            for (var _num_1 = 0; _num_1 < 16; _num_1 += 2) {
                if (pxInd < a.length) {
                    _num |= a[pxInd++] << _num_1;
                }
            }
            rqMsg += wordToStr(_num);
        }
    } else {
        if (c == -2) {
            while (pxInd < a.length && rqMsg.length < 1000) {
                var _num = 0;
                for (var _num_1 = 0; _num_1 < 16; _num_1 += 4) {
                    if (pxInd < a.length) {
                        _num |= a[pxInd++] << _num_1;
                    }
                }
                rqMsg += wordToStr(_num);
            }
        } else {
            while (pxInd < a.length && rqMsg.length < 1000) {
                var _num = 0;
                for (var _num_1 = 0; _num_1 < 8; _num_1++) {
                    if (pxInd < a.length && a[pxInd++] != c) {
                        _num |= 128 >> _num_1;
                    }
                }
                rqMsg += byteToStr(_num);
            }
        }
    }
    return u_show(a, k1, k2);
}
function u_line(a, c, k1, k2) {
    var x;
    rqMsg = '';
    while (rqMsg.length < 1000) {
        x = 0;
        while (x < 122) {
            var _num = 0;
            for (var _num_2 = 0; _num_2 < 8 && x < 122; _num_2++, x++) {
                if (a[pxInd++] != c) {
                    _num |= 128 >> _num_2;
                }
            }
            rqMsg += byteToStr(_num);
        }
    }
    return u_show(a, k1, k2);
}
function uploadImage() {
    var elm = getElm('canvas');
    var w = dispW = 400;
    var h = dispH = 300;
    var imageData = elm.getContext('2d').getImageData(0, 0, w, h);
    var array = new Array(w * h);
    var _num = 0;
    for (var _num_3 = 0; _num_3 < h; _num_3++) {
        for (var _num_4 = 0; _num_4 < w; _num_4++, _num++) {
            if (epdInd == 25 || epdInd == 37) {
                array[_num] = getVal_7color(imageData, _num << 2);
            } else {
                array[_num] = getVal(imageData, _num << 2);
            }
        }
    }
    dispX = 0;
    pxInd = 0;
    stInd = 0;
    xhReq = new XMLHttpRequest();
    rqPrf = 'http://192.168.8.22/';
    if (epdInd == 3 || epdInd == 39 || epdInd == 43) {
        xhReq.onload = xhReq.onerror = function () {
            if (stInd == 0) {
                return u_line(array, 0, 0, 100);
            }
            if (stInd == 1) {
                return u_done();
            }
        };
        if (epdInd > 25) {
            return u_send('EPD' + String.fromCharCode(epdInd + -26 + 65) + '_', false);
        }
        return u_send('EPD' + String.fromCharCode(epdInd + 97) + '_', false);
    }
    if (epdInd == 40) {
        xhReq.onload = xhReq.onerror = function () {
            if (stInd == 0) {
                return u_line(array, 0, 0, 50);
            }
            if (stInd == 1) {
                return u_next();
            }
            if (stInd == 2) {
                return u_line(array, 3, 50, 50);
            }
            if (stInd == 3) {
                return u_done();
            }
        };
        if (epdInd > 25) {
            return u_send('EPD' + String.fromCharCode(epdInd + -26 + 65) + '_', false);
        }
        return u_send('EPD' + String.fromCharCode(epdInd + 97) + '_', false);
    }
    if (epdInd == 0 || epdInd == 3 || epdInd == 6 || epdInd == 7 || epdInd == 9 || epdInd == 12 || epdInd == 16 || epdInd == 19 || epdInd == 22 || epdInd == 26 || epdInd == 27 || epdInd == 28) {
        xhReq.onload = xhReq.onerror = function () {
            if (stInd == 0) {
                return u_data(array, 0, 0, 100);
            }
            if (stInd == 1) {
                return u_done();
            }
        };
        if (epdInd > 25) {
            return u_send('EPD' + String.fromCharCode(epdInd + -26 + 65) + '_', false);
        }
        return u_send('EPD' + String.fromCharCode(epdInd + 97) + '_', false);
    }
    if (epdInd > 15 && epdInd < 22) {
        xhReq.onload = xhReq.onerror = function () {
            if (stInd == 0) {
                return u_data(array, -1, 0, 100);
            }
            if (stInd == 1) {
                return u_done();
            }
        };
        return u_send('EPD' + String.fromCharCode(epdInd + 97) + '_', false);
    }
    if (epdInd == 25 || epdInd == 37) {
        xhReq.onload = xhReq.onerror = function () {
            if (stInd == 0) {
                return u_data(array, -2, 0, 100);
            }
            if (stInd == 1) {
                return u_done();
            }
        };
        if (epdInd > 25) {
            return u_send('EPD' + String.fromCharCode(epdInd + -26 + 65) + '_', false);
        }
        return u_send('EPD' + String.fromCharCode(epdInd + 97) + '_', false);
    } else {
        xhReq.onload = xhReq.onerror = function () {
            console.log('*************');
            console.log(stInd);
            console.log('*************');
            if (stInd == 0 && epdInd == 23) {
                return u_data(array, 0, 0, 100);
            }
            if (stInd == 0) {
                return u_data(array, epdInd == 1 || epdInd == 12 ? -1 : 0, 0, 50);
            }
            if (stInd == 1) {
                return u_next();
            }
            if (stInd == 2) {
                return u_data(array, 3, 50, 50);
            }
            if (stInd == 3) {
                return u_done();
            }
        };
        if (epdInd > 25) {
            return u_send('EPD' + String.fromCharCode(epdInd + -26 + 65) + '_', false);
        }
        return u_send('EPD' + String.fromCharCode(epdInd + 97) + '_', false);
    }
}