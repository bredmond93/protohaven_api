/**
 * Registers a new block provided a unique name and an object defining its behavior.
 *
 * @see https://developer.wordpress.org/block-editor/reference-guides/block-api/block-registration/
 */
import { registerBlockType } from '@wordpress/blocks';

/**
 * Lets webpack process CSS, SASS or SCSS files referenced in JavaScript files.
 * All files containing `style` keyword are bundled together. The code used
 * gets applied both to the front of your site and to the editor.
 *
 * @see https://www.npmjs.com/package/@wordpress/scripts#using-css
 */
import './style.scss';

/**
 * Internal dependencies
 */
import Edit from './edit';
import metadata from './block.json';

const icon = (
<svg
   viewBox="0 0 850.49237 941.78455"
   xmlns="http://www.w3.org/2000/svg">

  <path
     style={{fill:"#fdfdfd"}}
     d="M 214.5678,756.88793 C 168.76442,750.27767 121.54372,719.28129 81.97004,669.84875 67.4664,651.73186 56.24397,634.28308 45.95286,613.84875 38.87436,599.79346 34.6637,589.52855 28.48815,571.27254 12.53265,524.1053 3.6586003,479.82579 0.51248032,431.68021 c -1.01834,-15.58367 -0.43249,-57.87566 0.99502998,-71.83146 6.08207,-59.45974 20.6703097,-110.00221 45.7537197,-158.51848 25.0538,-48.45902 57.77372,-88.8824 104.05047,-128.547725 45.30207,-38.82989 96.94821,-61.76691 156.61718,-69.5566496 75.06333,-9.79945 139.23097,2.74454 191.29612,37.3960496 42.54676,28.31662 72.58077,68.331515 86.41762,115.135855 4.64849,15.72394 6.86555,31.55855 7.40032,52.85439 1.02121,40.66733 -7.20098,75.98866 -26.17616,112.44892 -8.94146,17.18076 -22.97773,37.71316 -35.38019,51.7545 -29.97876,33.9402 -86.7074,62.95791 -138.20066,70.69208 -3.69015,0.55425 -7.71001,1.00773 -8.93303,1.00773 h -2.22367 l -1.1645,9.16666 c -3.65466,28.76846 -11.2315,79.84339 -16.78801,113.16667 -4.59304,27.54528 -14.17226,80.46719 -15.97125,88.23569 -3.39086,14.64268 -12.4979,35.85523 -20.79253,48.43098 -18.95474,28.73785 -44.01946,46.17384 -75.25943,52.35338 -9.34081,1.8477 -28.28515,2.36137 -37.58571,1.01913 z m 23.23718,-56.71535 c 16.26356,-5.13765 25.52207,-18.64022 32.44924,-47.32383 3.02089,-12.50871 4.90995,-22.99541 9.2621,-51.41665 5.37645,-35.11031 11.0857,-75.78318 20.13313,-143.42917 0.94495,-7.0652 1.54756,-13.2902 1.33914,-13.83333 -0.20909,-0.54488 -1.21049,-0.98752 -2.2341,-0.98752 -7.16183,0 -46.12882,-6.83142 -62.43736,-10.94609 -19.35306,-4.8828 -27.27234,-8.65666 -35.78682,-17.05391 -2.80525,-2.76662 -5.72741,-6.38346 -6.54202,-8.09724 -2.82316,-5.93935 -3.29186,-14.14404 -1.28931,-22.56942 1.84327,-7.75524 8.40803,-15.8227 15.52787,-19.08227 8.83576,-4.04514 16.95604,-3.6666 37.10351,1.72964 20.97448,5.61774 45.33941,10.62197 60.04678,12.33279 3.60378,0.4192 3.82846,0.35974 4.16349,-1.10186 0.42993,-1.87565 15.67454,-110.48919 20.33459,-144.8783 4.38433,-32.35434 4.74786,-34.19443 8.08872,-40.94292 5.10023,-10.30237 15.47056,-18.40502 27.02009,-21.1116 7.07163,-1.6572 19.14373,-1.03957 25.16872,1.28769 14.02115,5.41593 22.35736,17.52204 22.40347,32.53507 0.0123,3.99884 -2.67741,24.87943 -15.04508,116.79753 -4.23538,31.47784 -7.60528,57.3253 -7.48868,57.43879 0.1166,0.11349 3.06201,-0.21392 6.54534,-0.72758 34.38983,-5.07123 63.27765,-22.44141 86.06619,-51.75139 20.66914,-26.58407 32.31532,-54.43981 37.03571,-88.58332 1.596,-11.54414 1.59562,-34.75503 -7.4e-4,-45.53821 -5.9259,-40.02855 -25.21753,-70.31795 -58.62233,-92.04172 -55.24953,-35.929805 -124.50159,-35.888695 -196.81216,0.11684 -34.37102,17.11433 -59.09494,36.51651 -84.32716,66.17605 -24.82375,29.17939 -47.72076,71.20905 -62.65616,115.01143 -31.94221,93.67971 -32.60557,210.791 -1.67666,296 19.01463,52.3852 49.47068,94.33218 82.99331,114.30631 14.74575,8.78611 27.71118,11.32525 39.23718,7.68419 z"
     id="path8" />
  <path
     style={{fill:"#f2c244"}}
     d="m 267.23447,793.83245 c -31.73007,-4.4055 -61.93849,-18.9981 -92.8102,-44.83343 -4.2956,-3.59482 -7.96649,-6.78895 -8.15754,-7.09806 -0.19104,-0.30912 2.8786,0.87745 6.82142,2.63682 21.76722,9.71296 41.45387,13.88967 61.81298,13.11419 38.34714,-1.46065 69.97606,-19.96943 92.51181,-54.13655 8.29463,-12.57575 17.40167,-33.7883 20.79253,-48.43098 1.79899,-7.7685 11.37821,-60.69041 15.97125,-88.23569 5.55651,-33.32328 13.13335,-84.39821 16.78801,-113.16667 l 1.1645,-9.16666 h 2.22367 c 1.22302,0 5.24288,-0.45348 8.93303,-1.00773 51.49326,-7.73417 108.2219,-36.75188 138.20066,-70.69208 21.35316,-24.17481 40.03816,-56.20603 49.95318,-85.63353 8.7864,-26.07777 12.3204,-50.00793 11.60317,-78.56989 -0.83545,-33.2698 -6.22754,-56.53904 -19.41018,-83.76344 -9.42825,-19.47095 -20.88595,-35.911415 -37.14875,-53.304095 l -5.58288,-5.97076 5.33334,2.89236 c 21.39359,11.6021 46.64966,32.657605 62.43295,52.049165 24.94559,30.64847 39.05644,62.74068 44.26283,100.66666 1.4337,10.44379 2.01673,38 1.04399,49.34314 -4.0633,47.38228 -22.229,90.86933 -55.06118,131.81157 -16.86055,21.02536 -39.24914,38.36488 -68.67859,53.19021 -27.12505,13.66447 -57.5242,23.12946 -81.99823,25.53072 l -4.66489,0.4577 -1.50505,11.33333 c -3.07579,23.16136 -8.92741,63.62738 -12.16927,84.15475 -7.18268,45.48058 -18.84111,110.01778 -21.64964,119.84525 -13.06741,45.72486 -42.14935,79.2182 -79.60951,91.6853 -12.97814,4.3192 -19.32775,5.3728 -34.07008,5.6529 -7.15,0.1359 -14.95,-0.024 -17.33333,-0.3545 z m -45.5,-92.42522 c 0.45833,-0.18494 1.20833,-0.18494 1.66666,0 0.45834,0.18494 0.0833,0.33626 -0.83333,0.33626 -0.91667,0 -1.29167,-0.15132 -0.83333,-0.33626 z m 10.04166,-0.0139 c 0.48125,-0.19258 1.05625,-0.1689 1.27778,0.0526 0.22153,0.22153 -0.17222,0.3791 -0.875,0.35015 -0.77663,-0.032 -0.9346,-0.18996 -0.40278,-0.40278 z m -22.875,-3.7453 C 181.72657,686.54919 151.23708,653.70385 130.72792,613.43455 91.13854,535.70166 81.69934,422.62057 106.24105,320.08329 c 10.72655,-44.81639 29.95308,-90.1193 53.22627,-125.41548 23.59507,-35.78435 53.17732,-64.4208 87.10048,-84.31571 15.67494,-9.19288 39.89957,-20.107475 56.33333,-25.381415 52.77226,-16.93572 101.24878,-14.39296 143.47883,7.52595 10.05091,5.21679 18.13271,10.327815 25.90662,16.383665 6.36849,4.96105 16.73446,14.73743 16.19654,15.27535 -0.20737,0.20737 -1.99815,-0.33819 -3.97951,-1.21234 -10.37776,-4.57857 -28.50747,-9.27375 -43.26914,-11.20571 -8.30584,-1.08705 -32.3834,-1.07303 -41.66667,0.0243 -48.49424,5.73203 -101.79279,29.63026 -139.26002,62.44199 -47.615,41.69859 -83.65816,105.63506 -102.3994,181.6449 -12.74615,51.69524 -16.80892,111.12823 -11.302,165.33333 7.09553,69.84189 28.30477,128.04656 62.12865,170.5 3.57864,4.49167 6.28,8.16162 6.00303,8.15546 -0.27698,-0.006 -2.90359,-0.99145 -5.83693,-2.1895 z m 87.77193,-219.79928 c 0,-0.91667 0.15132,-1.29167 0.33626,-0.83333 0.18494,0.45833 0.18494,1.20833 0,1.66666 -0.18494,0.45834 -0.33626,0.0833 -0.33626,-0.83333 z m 0.63874,-5.01508 c -0.0614,-1.071 -0.84684,-1.52731 -3.81772,-2.21801 -20.82045,-4.84057 -32.25134,-9.77236 -40.4956,-17.47159 -2.82903,-2.642 -5.87215,-6.04667 -6.76249,-7.56592 -1.47092,-2.50994 -4.08445,-10.88262 -3.55487,-11.38838 0.12101,-0.11557 3.64642,0.49964 7.83424,1.36711 10.4299,2.16048 29.86283,5.36854 40.71911,6.72206 4.95,0.61715 9.27066,1.35848 9.60146,1.64741 0.35308,0.30839 -0.14854,6.25108 -1.2147,14.39053 -1.99686,15.24471 -2.19592,16.49596 -2.30943,14.51679 z m -97.78594,-57.81825 -1.95806,-2.16667 2.16667,1.95806 c 2.01963,1.82519 2.4731,2.37527 1.95806,2.37527 -0.11474,0 -1.08974,-0.975 -2.16667,-2.16666 z m -8.18613,-15.83334 c 0,-0.91666 0.15132,-1.29166 0.33626,-0.83333 0.18494,0.45833 0.18494,1.20833 0,1.66667 -0.18494,0.45833 -0.33626,0.0833 -0.33626,-0.83334 z m 0,-9.33333 c 0,-0.91667 0.15132,-1.29167 0.33626,-0.83333 0.18494,0.45833 0.18494,1.20833 0,1.66666 -0.18494,0.45834 -0.33626,0.0833 -0.33626,-0.83333 z m 198.5614,-10.59712 c 0,-0.34239 3.44503,-26.22311 7.65562,-57.5127 4.2106,-31.2896 9.29288,-69.31152 11.29396,-84.49316 2.46172,-18.67639 3.92056,-27.77956 4.51104,-28.14899 1.8161,-1.13623 8.41442,-2.13806 13.87736,-2.10703 10.75131,0.0611 20.12935,3.73181 26.936,10.54322 7.0074,7.0123 10.07048,15.40835 9.58781,26.28068 -0.15549,3.50264 -3.55821,30.87618 -7.56159,60.8301 l -7.27887,54.46167 -5.01066,3.01695 c -14.037,8.45177 -32.07816,14.77786 -47.67733,16.71794 -1.83334,0.22801 -4.00834,0.5539 -4.83334,0.72421 -0.825,0.1703 -1.5,0.0295 -1.5,-0.31289 z m -190,-8.40288 c 0.86117,-0.91667 1.71576,-1.66667 1.89909,-1.66667 0.18333,0 -0.37126,0.75 -1.23242,1.66667 -0.86116,0.91667 -1.71575,1.66667 -1.89909,1.66667 -0.18333,0 0.37126,-0.75 1.23242,-1.66667 z m 15.875,-8.12208 c 0.48125,-0.19258 1.05625,-0.16889 1.27778,0.0526 0.22153,0.22152 -0.17222,0.37909 -0.875,0.35014 -0.77663,-0.032 -0.9346,-0.18996 -0.40278,-0.40278 z M 462.5678,348.26371 c 0,-0.13843 0.525,-0.66343 1.16667,-1.16666 1.05737,-0.82925 1.08095,-0.80567 0.2517,0.2517 -0.87091,1.1105 -1.41837,1.46365 -1.41837,0.91496 z m 11.66667,-11.74829 c 0.66365,-0.73334 1.35665,-1.33334 1.53998,-1.33334 0.18333,0 -0.20966,0.6 -0.87332,1.33334 -0.66365,0.73333 -1.35665,1.33333 -1.53998,1.33333 -0.18333,0 0.20966,-0.6 0.87332,-1.33333 z m -102.5,-166.47049 c 0.825,-0.1589 2.175,-0.1589 3,0 0.825,0.1589 0.15,0.28891 -1.5,0.28891 -1.65,0 -2.325,-0.13001 -1.5,-0.28891 z"
     id="path6" />
  <path
     style={{fill:"#ef5d21"}}
     d="m 315.3526,830.13525 c -23.16602,-3.7325 -46.04563,-13.3535 -69.45147,-29.2046 -6.91745,-4.6847 -20.18138,-15.088 -26,-20.3927 l -3,-2.735 3.64461,1.7741 c 6.40722,3.1188 17.93795,7.5419 24.91707,9.5579 15.10939,4.3646 25.8612,5.7174 41.09658,5.171 12.56736,-0.4508 20.23592,-1.8306 32.07849,-5.7719 37.46016,-12.4671 66.5421,-45.96044 79.60951,-91.6853 2.80853,-9.82747 14.46696,-74.36467 21.64964,-119.84525 3.24186,-20.52737 9.09348,-60.99339 12.16927,-84.15475 l 1.50505,-11.33333 4.66489,-0.4577 c 24.47403,-2.40126 54.87318,-11.86625 81.99823,-25.53072 29.42945,-14.82533 51.81804,-32.16485 68.67859,-53.19021 32.83218,-40.94224 50.99788,-84.42929 55.06118,-131.81157 0.97274,-11.34314 0.38971,-38.89935 -1.04399,-49.34314 -3.09778,-22.5658 -8.44245,-40.33967 -17.99136,-59.83088 -9.58277,-19.56035 -21.01244,-35.92057 -37.12155,-53.1351 l -5.58287,-5.96598 4,2.24585 c 52.03005,29.21294 89.51627,75.96744 103.3023,128.84328 4.98719,19.1282 6.61844,34.89664 6.15628,59.5095 -0.48508,25.8334 -3.39344,43.55548 -10.82781,65.9793 -7.20925,21.74481 -15.47687,38.47649 -29.32857,59.35403 -17.26769,26.02618 -33.68859,42.93266 -56.63554,58.31028 -18.81726,12.61017 -40.75167,23.32366 -62.89328,30.71915 -16.67402,5.56928 -26.22956,7.71231 -49.1233,11.01693 l -2.01659,0.29108 -2.51698,19.16462 c -6.00218,45.70137 -14.99155,102.35536 -24.77887,156.16461 -6.82873,37.5434 -7.93329,42.10561 -13.76484,56.85347 -16.55124,41.85773 -47.99792,70.04403 -87.5728,78.49323 -8.96544,1.9141 -31.60441,2.4345 -40.88187,0.9398 z M 222.23447,701.41788 c -6.39664,-1.01258 -6.75656,-1.2725 -13.52457,-9.76729 -46.89427,-58.85883 -69.9898,-150.65712 -63.43467,-252.13517 7.10415,-109.97741 49.61352,-208.0212 115.03255,-265.31157 32.72731,-28.66078 79.02572,-51.33456 121.68377,-59.59235 15.16533,-2.93573 23.36208,-3.7172 38.90958,-3.70962 20.42397,0.01 35.3841,2.33803 53,8.24776 13.9491,4.6796 15.3015,5.38886 18.77588,9.84692 3.77885,4.84872 8.98089,12.6718 11.82471,17.78256 l 2.18701,3.93038 -2.56046,-0.45042 c -32.30258,-5.68244 -65.14678,-2.75914 -100.22714,8.92072 -6.41666,2.1364 -15.21827,5.4109 -19.55913,7.27666 -4.42091,1.90017 -8.90514,3.39229 -10.19477,3.39229 -4.51288,0 -12.66398,2.12876 -18.04292,4.71212 -5.83835,2.80401 -12.21181,8.12226 -15.55217,12.9773 -1.16525,1.69364 -4.88058,4.89079 -9.45212,8.13384 -20.39543,14.46847 -41.40177,35.17306 -58.01004,57.17674 -20.95484,27.76227 -39.27521,62.91339 -51.87433,99.5308 l -3.39282,9.86072 -4.63672,1.19445 c -14.17123,3.65059 -22.69985,16.67785 -21.82542,33.3378 0.37701,7.18303 3.00345,12.87257 8.46222,18.33134 l 3.75721,3.75721 -1.44327,8.99384 c -9.35082,58.27039 -8.57762,119.8105 2.16935,172.66051 6.86093,33.73977 17.98513,65.80334 31.43816,90.61502 2.10289,3.87841 3.82344,7.32145 3.82344,7.65122 0,1.70141 -11.85179,3.50395 -17.33333,2.63622 z m 73.15785,-223.97981 c -1.25581,-4.17934 -1.08691,-6.25599 0.50881,-6.25599 1.11032,0 1.32014,0.41816 1.25446,2.5 -0.0434,1.375 -0.27235,3.4 -0.50881,4.5 l -0.42994,2 z M 449.23447,357.59724 c 0,-0.74995 12.31465,-94.18269 14.35251,-108.89423 0.3522,-2.54256 0.62583,-2.88383 2.85186,-3.55677 1.35426,-0.4094 5.50279,-0.90661 9.21896,-1.1049 12.72864,-0.67921 22.78404,2.96707 30.33946,11.00167 2.33046,2.47826 4.96217,6.07058 5.84824,7.98293 1.60837,3.47123 1.60912,3.48392 0.45275,7.6499 -7.41923,26.72897 -29.28492,60.42488 -51.02972,78.63886 -8.49515,7.11574 -12.03406,9.55143 -12.03406,8.28254 z"
     id="path5" />
  <path
     style={{fill:"#744784"}}
     d="m 379.23447,868.06885 c -21.27777,-1.1613 -43.7172,-8.0425 -65.66667,-20.1372 -12.37235,-6.8175 -31.392,-20.5136 -41.66667,-30.0044 l -3.66666,-3.3869 6.33333,2.9232 c 13.86922,6.4013 28.00694,10.691 42.06412,12.7631 10.34439,1.5248 29.94548,1.0103 39.60255,-1.0395 39.51045,-8.3864 71.02167,-36.6275 87.5728,-78.48493 5.83155,-14.74786 6.93611,-19.31007 13.76484,-56.85347 9.78732,-53.80925 18.77669,-110.46324 24.77887,-156.16461 l 2.51698,-19.16462 2.01659,-0.29108 c 22.89374,-3.30462 32.44928,-5.44765 49.1233,-11.01693 35.10308,-11.72474 67.32752,-30.55458 90.13846,-52.67095 16.99515,-16.47767 36.48477,-44.33598 47.80098,-68.32634 10.10266,-21.41763 16.42249,-42.33696 20.04932,-66.36547 1.95295,-12.93871 2.43782,-41.15296 0.95091,-55.33333 -2.71818,-25.92286 -8.00081,-44.73275 -18.66224,-66.45085 -9.75664,-19.87498 -19.29566,-33.64128 -35.70431,-51.52694 l -7.01317,-7.64446 4.66667,2.5831 c 23.16966,12.82492 46.67239,32.34099 63.07093,52.37248 33.7397,41.21449 48.4393,86.96793 45.8349,142.66419 -2.3271,49.76504 -21.34701,97.3164 -56.092,140.23458 -23.1702,28.62061 -61.05561,53.05176 -105.03551,67.73422 -11.2595,3.75892 -27.4354,7.64868 -37.44499,9.00426 -13.49703,1.82787 -12.19187,0.96419 -13.17742,8.72011 -6.1285,48.2288 -15.69947,109.31706 -26.1791,167.09235 -6.26307,34.52895 -7.17681,38.66299 -11.09921,50.21699 -12.06144,35.5284 -35.47425,63.7005 -64.54427,77.6645 -7.66263,3.6808 -18.92701,7.4398 -26.69375,8.908 -7.44735,1.4077 -20.71668,2.3587 -27.63958,1.9809 z M 236.02509,691.68208 c -36.64434,-67.58676 -49.22784,-164.85995 -34.02234,-263 0.80954,-5.225 1.73787,-9.5 2.06296,-9.5 0.32508,0 1.55155,0.73261 2.7255,1.62803 5.56157,4.24202 16.12201,8.41339 29.56848,11.67955 l 6.12523,1.48782 0.72381,3.37498 c 1.19994,5.59515 3.10943,9.03348 7.6144,13.71093 l 4.28787,4.45203 -0.93951,5.33333 c -2.62962,14.92755 -5.06283,35.7661 -6.25313,53.55303 -0.88856,13.27811 -0.87832,49.63525 0.0178,63.17683 1.98999,30.07155 7.12747,61.43044 14.1881,86.60347 l 2.24387,8 -1.56114,3.57011 c -4.19756,9.59919 -10.85958,17.44282 -18.08698,21.29498 -2.20302,1.1742 -4.14569,2.13491 -4.31702,2.13491 -0.17134,0 -2.14139,-3.375 -4.37789,-7.5 z m 38.20938,-317.61657 c -0.73334,-0.17527 -5.68334,-1.34435 -11,-2.59796 -5.31667,-1.25361 -14.91667,-3.65408 -21.33334,-5.33437 -7.9052,-2.07009 -13.65487,-3.17737 -17.83333,-3.43437 -3.39167,-0.20861 -6.16667,-0.44823 -6.16667,-0.53249 0,-0.0843 1.36536,-4.13935 3.03413,-9.01129 12.62813,-36.86761 30.81346,-71.88231 51.94457,-100.01599 16.79869,-22.36555 39.41068,-44.50243 60.17037,-58.9061 l 5.48241,-3.80386 -1.59646,3.60988 c -2.50138,5.65606 -2.73469,6.94299 -7.33804,40.47646 -2.3909,17.41666 -5.20905,37.82324 -6.26256,45.34795 l -1.91547,13.68128 -5.09127,7.41388 c -11.55146,16.82116 -26.89217,45.35041 -34.89268,64.89022 -3.50747,8.56636 -3.89393,9.0073 -7.20166,8.21676 z m 231.29139,-119.71676 -1.95806,-2.16667 2.16667,1.95806 c 2.01963,1.82519 2.4731,2.37528 1.95806,2.37528 -0.11474,0 -1.08974,-0.975 -2.16667,-2.16667 z M 412.5678,204.65548 c 0,-17.14012 -11.81748,-30.78802 -29.30179,-33.84038 -3.07892,-0.5375 -5.69055,-1.06981 -5.80364,-1.18289 -0.46436,-0.46436 17.50424,-7.5466 27.43876,-10.81486 33.823,-11.12707 66.99218,-14.14898 97.24906,-8.85997 l 4.5824,0.80102 1.96526,4.37851 c 3.54433,7.89655 9.16752,25.55026 9.19861,28.87851 0.003,0.275 -1.80715,0.5 -4.0216,0.5 -8.56132,0 -26.5737,2.63628 -39.19665,5.7368 -12.81276,3.14714 -27.16984,7.95696 -40.11041,13.43755 -4.39373,1.86083 -8.13013,2.91739 -12.20037,3.44995 -3.22686,0.42221 -6.62139,1.05447 -7.5434,1.40501 -0.922,0.35054 -1.80683,0.63735 -1.9663,0.63735 -0.15946,0 -0.28993,-2.03697 -0.28993,-4.5266 z"
     id="path4" />
  <path
     style={{fill:"#349e5d"}}
     d="m 481.40113,941.38915 c 0.64167,-0.1676 1.69167,-0.1676 2.33334,0 0.64166,0.1677 0.11666,0.3049 -1.16667,0.3049 -1.28333,0 -1.80833,-0.1372 -1.16667,-0.3049 z m 9.33334,0 c 0.64166,-0.1676 1.69166,-0.1676 2.33333,0 0.64167,0.1677 0.11667,0.3049 -1.16667,0.3049 -1.28333,0 -1.80833,-0.1372 -1.16666,-0.3049 z m -65.26373,-36.9345 c -18.4457,-1.6461 -40.77313,-8.8272 -59.08234,-19.0023 -14.17541,-7.8778 -32.29547,-20.834 -43.15393,-30.8559 l -3.66667,-3.3842 7,3.2525 c 16.49928,7.6663 33.53774,12.2159 49.88337,13.3198 20.10961,1.3581 39.8383,-2.3048 57.11663,-10.6046 29.07002,-13.964 52.48283,-42.1361 64.54427,-77.6645 3.9224,-11.554 4.83614,-15.68804 11.09921,-50.21699 10.47963,-57.77529 20.0506,-118.86355 26.1791,-167.09235 0.98555,-7.75592 -0.31961,-6.89224 13.17742,-8.72011 38.01089,-5.14773 85.04784,-25.77678 116.6762,-51.1708 31.50473,-25.29476 60.80485,-70.8603 73.2905,-113.97641 11.8011,-40.75195 11.9149,-87.25656 0.3075,-125.62456 -8.64497,-28.57565 -23.91646,-54.45035 -46.91057,-79.48122 -6.89771,-7.50869 -6.94944,-7.58918 -3.67984,-5.72583 17.38093,9.90543 29.78521,18.77908 43.61401,31.20019 3.0972,2.78186 5.8796,4.90441 6.1832,4.71677 0.3036,-0.18764 0.4696,-0.0571 0.3689,0.2901 -0.1008,0.3472 2.3833,3.4445 5.5201,6.88289 30.2514,33.15933 47.6862,69.22978 52.9168,109.47829 8.3954,64.60076 -8.8623,125.0931 -51.1444,179.27343 -8.1908,10.49566 -14.949,17.68051 -23.70461,25.20112 -27.26866,23.42232 -65.91211,42.93805 -102.91369,51.9735 -6.91478,1.68853 -11.381,2.50258 -28.50009,5.19468 l -2.976,0.46799 -1.19327,9.33131 c -2.1118,16.51415 -7.1574,52.11204 -10.25214,72.3313 -6.78283,44.31508 -20.00499,118.9988 -23.30739,131.6489 -10.00528,38.3259 -34.66704,71.3533 -64.89912,86.9139 -13.30099,6.846 -26.9687,10.7362 -42.39609,12.0668 -8.89795,0.7674 -11.26289,0.7646 -20.09706,-0.024 z M 261.69597,662.64248 c -7.11962,-26.47015 -11.79509,-55.37412 -13.75982,-85.06387 -1.51355,-22.87192 -0.78607,-59.27283 1.66003,-83.06319 1.64736,-16.02195 4.8004,-37.25871 5.67805,-38.24361 0.28276,-0.31732 1.51449,0.17496 2.73718,1.09395 5.61825,4.22276 16.70351,8.62157 29.72948,11.79713 5.63029,1.37259 6.20375,1.65942 6.52178,3.26205 0.19178,0.96643 0.77741,3.23249 1.3014,5.03569 0.91073,3.13412 0.70316,5.07243 -4.7121,44 -13.27039,95.39434 -18.17062,124.61592 -23.96645,142.91929 -1.30077,4.10786 -2.4434,7.46883 -2.53919,7.46883 -0.0958,0 -1.28845,-4.14282 -2.65036,-9.20627 z M 849.2871,416.79319 c 0.032,-0.77662 0.19,-0.9346 0.4028,-0.40277 0.1926,0.48125 0.1689,1.05625 -0.053,1.27777 -0.2215,0.22153 -0.379,-0.17222 -0.3501,-0.875 z m 0.8709,-18.27777 c 0,-4.58334 0.1066,-6.45834 0.2367,-4.16667 0.1302,2.29167 0.1302,6.04167 0,8.33333 -0.1301,2.29167 -0.2367,0.41667 -0.2367,-4.16666 z M 297.5678,378.14325 c -16.27977,-2.43113 -19.37182,-3.1638 -19.13103,-4.53318 0.94995,-5.40233 17.92628,-40.30962 26.99384,-55.5056 5.95705,-9.9832 15.14086,-23.8076 15.54643,-23.40204 0.13327,0.13327 -2.45295,19.12071 -5.74716,42.19432 -3.29421,23.0736 -5.99081,42.177 -5.99244,42.452 -0.002,0.275 -0.22797,0.47467 -0.50297,0.4437 -0.275,-0.031 -5.3,-0.7731 -11.16667,-1.6492 z m 166.33333,-136.8211 c 0,-15.88016 -10.40322,-28.96279 -26.32975,-33.11112 -2.17271,-0.56592 -5.08735,-1.02895 -6.47698,-1.02895 -2.60989,0 -3.41345,-0.90669 -1.35993,-1.5345 0.64166,-0.19617 4.76666,-1.84282 9.16666,-3.65922 20.98826,-8.66433 42.9497,-14.36707 64.66667,-16.79203 9.52785,-1.0639 14.17419,-0.90929 14.59749,0.48575 1.68153,5.54168 3.26359,26.89046 2.66769,35.99878 l -0.44697,6.83212 -2.74244,0.71459 c -11.97048,3.11912 -37.77582,13.10039 -36.29557,14.03879 0.52468,0.33262 -1.29021,0.56937 -4.44687,0.58009 -2.93333,0.01 -6.98333,0.461 -9,1.0023 -2.01666,0.5413 -3.74166,0.98774 -3.83333,0.99209 -0.0917,0.004 -0.16667,-2.02906 -0.16667,-4.51869 z"
     id="path3" />
  <path
     style={{fill:"#01777a"}}
     d="m 477.90113,941.14385 c -18.95245,-1.386 -40.93822,-8.3866 -60.84748,-19.3749 -12.99047,-7.1697 -31.3193,-20.2172 -41.48585,-29.5319 l -4,-3.6648 8.33333,3.5679 c 23.35299,9.9987 44.71103,14.0828 64.82384,12.3958 28.09481,-2.3566 50.90878,-12.8404 70.69728,-32.4879 17.44127,-17.317 30.77536,-41.0182 37.44076,-66.5504 3.3024,-12.6501 16.52456,-87.33382 23.30739,-131.6489 3.09474,-20.21926 8.14034,-55.81715 10.25214,-72.3313 l 1.19327,-9.33131 2.976,-0.46799 c 17.11909,-2.6921 21.58531,-3.50615 28.50009,-5.19468 43.71852,-10.67567 90.82401,-36.83084 115.8551,-64.32816 26.3563,-28.95316 47.7111,-68.0456 56.9196,-104.19817 9.7524,-38.28775 9.3446,-82.26338 -1.0832,-116.81506 -9.0778,-30.07864 -24.1129,-55.80708 -47.43,-81.16351 l -6.8939,-7.49686 4.8875,2.76597 c 26.2606,14.86163 49.4459,34.67849 66.7561,57.0574 18.2666,23.61528 32.4861,53.83971 37.7173,80.17034 2.7616,13.90028 3.5283,22.01965 3.8715,41 0.2622,14.49792 0.095,20.97436 -0.748,29 -3.9515,37.61386 -17.0114,72.84406 -39.4182,106.33333 -7.8021,11.66107 -15.925,22.15192 -23.4319,30.26268 -29.6304,32.01415 -84.81014,60.14759 -132.22793,67.4166 -4.93061,0.75585 -10.31471,1.59011 -11.96468,1.8539 l -2.99995,0.47963 -0.51289,4.32693 c -6.63186,55.94857 -28.62011,189.27286 -34.85269,211.32696 -14.1885,50.2062 -48.90719,85.8235 -92.27271,94.6608 -5.38709,1.0978 -23.32633,2.8922 -25.69515,2.5702 -0.36667,-0.05 -3.81667,-0.321 -7.66667,-0.6026 z m 34.01359,-678.51658 c -3.68164,-8.3865 -14.39506,-16.26113 -24.68025,-18.1406 -7.67701,-1.40286 -7.67423,-1.41142 1.71558,-5.27556 7.74837,-3.18863 25.16935,-9.21169 29.72053,-10.27545 1.73518,-0.40557 1.76334,-0.35876 1.4539,2.41642 -1.23588,11.08387 -3.81274,25.2278 -6.06117,33.26873 -0.47045,1.68243 -0.57912,1.58161 -2.14859,-1.99354 z"
     id="path2" />

</svg>
);

/**
 * Every block starts by registering a new block type definition.
 *
 * @see https://developer.wordpress.org/block-editor/reference-guides/block-api/block-registration/
 */
registerBlockType( metadata.name, {
	icon, edit: Edit,
} );
