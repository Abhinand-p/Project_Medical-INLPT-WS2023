"use strict";
/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
self["webpackHotUpdate_N_E"]("pages/chatRoom",{

/***/ "./src/components/chatBox.tsx":
/*!************************************!*\
  !*** ./src/components/chatBox.tsx ***!
  \************************************/
/***/ (function(module, __webpack_exports__, __webpack_require__) {

eval(__webpack_require__.ts("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-dev-runtime */ \"./node_modules/react/jsx-dev-runtime.js\");\n/* harmony import */ var react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ \"./node_modules/react/index.js\");\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var _barrel_optimize_names_Box_Button_List_ListItem_ListItemText_TextField_Typography_mui_material__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! __barrel_optimize__?names=Box,Button,List,ListItem,ListItemText,TextField,Typography!=!@mui/material */ \"__barrel_optimize__?names=Box,Button,List,ListItem,ListItemText,TextField,Typography!=!./node_modules/@mui/material/index.js\");\n\nvar _s = $RefreshSig$();\n\n\nconst MAX_CHARACTERS = 4000;\nconst ChatComponent = ()=>{\n    _s();\n    const [messages, setMessages] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)([]);\n    const [newMessage, setNewMessage] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(\"\");\n    const [data, setData] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(\"\");\n    const request = new Request(\"http://127.0.0.1:8000/get-answer-from-local\", {\n        method: \"POST\",\n        headers: {\n            \"Content-Type\": \"application/json\"\n        },\n        body: JSON.stringify({\n            question: newMessage\n        })\n    });\n    async function handleSendMessage() {\n        console.log(newMessage);\n        setMessages([\n            ...messages,\n            {\n                text: newMessage,\n                type: \"user\"\n            }\n        ]);\n        setNewMessage(\"\");\n        try {\n            const response = await fetch(request);\n            const data = await response.json();\n            console.log(data);\n            if (response.status === 200) {\n                setMessages((prevMessages)=>[\n                        ...prevMessages,\n                        {\n                            text: data,\n                            type: \"assistant\"\n                        }\n                    ]);\n            } else {\n                console.log(\"Something went wrong\");\n            }\n        } catch (error) {\n            console.log(error);\n        }\n    }\n    return /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_barrel_optimize_names_Box_Button_List_ListItem_ListItemText_TextField_Typography_mui_material__WEBPACK_IMPORTED_MODULE_2__.Box, {\n        sx: {\n            display: \"flex\",\n            flexDirection: \"column\",\n            height: \"50%\",\n            width: \"50%\",\n            position: \"absolute\",\n            top: \"50%\",\n            left: \"50%\",\n            transform: \"translate(-50%, -50%)\",\n            border: \"1px solid gray\",\n            borderRadius: \"10px\"\n        },\n        children: [\n            /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_barrel_optimize_names_Box_Button_List_ListItem_ListItemText_TextField_Typography_mui_material__WEBPACK_IMPORTED_MODULE_2__.Box, {\n                sx: {\n                    overflow: \"auto\",\n                    flexGrow: 1\n                },\n                children: /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_barrel_optimize_names_Box_Button_List_ListItem_ListItemText_TextField_Typography_mui_material__WEBPACK_IMPORTED_MODULE_2__.List, {\n                    children: messages.map((message, index)=>/*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_barrel_optimize_names_Box_Button_List_ListItem_ListItemText_TextField_Typography_mui_material__WEBPACK_IMPORTED_MODULE_2__.ListItem, {\n                            sx: {\n                                justifyContent: message.type === \"user\" ? \"flex-end\" : \"flex-start\"\n                            },\n                            children: /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_barrel_optimize_names_Box_Button_List_ListItem_ListItemText_TextField_Typography_mui_material__WEBPACK_IMPORTED_MODULE_2__.ListItemText, {\n                                sx: {\n                                    textAlign: message.type === \"user\" ? \"right\" : \"left\"\n                                },\n                                primary: /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_barrel_optimize_names_Box_Button_List_ListItem_ListItemText_TextField_Typography_mui_material__WEBPACK_IMPORTED_MODULE_2__.Typography, {\n                                    variant: \"body1\",\n                                    sx: {\n                                        backgroundColor: message.type === \"user\" ? \"lightblue\" : \"grey\",\n                                        padding: \"5px\",\n                                        borderRadius: \"10px\",\n                                        display: \"inline-block\"\n                                    },\n                                    children: message.text\n                                }, void 0, false, void 0, void 0)\n                            }, void 0, false, {\n                                fileName: \"/home/john/INLPT/Project_Medical-INLPT-WS2023/server/frontend/src/components/chatBox.tsx\",\n                                lineNumber: 81,\n                                columnNumber: 15\n                            }, undefined)\n                        }, index, false, {\n                            fileName: \"/home/john/INLPT/Project_Medical-INLPT-WS2023/server/frontend/src/components/chatBox.tsx\",\n                            lineNumber: 74,\n                            columnNumber: 13\n                        }, undefined))\n                }, void 0, false, {\n                    fileName: \"/home/john/INLPT/Project_Medical-INLPT-WS2023/server/frontend/src/components/chatBox.tsx\",\n                    lineNumber: 72,\n                    columnNumber: 9\n                }, undefined)\n            }, void 0, false, {\n                fileName: \"/home/john/INLPT/Project_Medical-INLPT-WS2023/server/frontend/src/components/chatBox.tsx\",\n                lineNumber: 71,\n                columnNumber: 7\n            }, undefined),\n            /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_barrel_optimize_names_Box_Button_List_ListItem_ListItemText_TextField_Typography_mui_material__WEBPACK_IMPORTED_MODULE_2__.Box, {\n                sx: {\n                    display: \"flex\",\n                    alignItems: \"center\",\n                    padding: 1,\n                    borderTop: \"1px solid gray\"\n                },\n                children: [\n                    /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_barrel_optimize_names_Box_Button_List_ListItem_ListItemText_TextField_Typography_mui_material__WEBPACK_IMPORTED_MODULE_2__.TextField, {\n                        value: newMessage,\n                        onChange: (e)=>{\n                            setNewMessage(e.target.value);\n                        },\n                        variant: \"outlined\",\n                        placeholder: \"Write a message\",\n                        sx: {\n                            flexGrow: 1,\n                            marginRight: 1,\n                            borderColor: \"primary.main\",\n                            borderWidth: 2,\n                            borderRadius: \"5px\"\n                        },\n                        inputProps: {\n                            maxLength: MAX_CHARACTERS\n                        }\n                    }, void 0, false, {\n                        fileName: \"/home/john/INLPT/Project_Medical-INLPT-WS2023/server/frontend/src/components/chatBox.tsx\",\n                        lineNumber: 112,\n                        columnNumber: 9\n                    }, undefined),\n                    /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_barrel_optimize_names_Box_Button_List_ListItem_ListItemText_TextField_Typography_mui_material__WEBPACK_IMPORTED_MODULE_2__.Typography, {\n                        variant: \"body2\",\n                        children: [\n                            MAX_CHARACTERS - newMessage.length,\n                            \"/4000\"\n                        ]\n                    }, void 0, true, {\n                        fileName: \"/home/john/INLPT/Project_Medical-INLPT-WS2023/server/frontend/src/components/chatBox.tsx\",\n                        lineNumber: 128,\n                        columnNumber: 9\n                    }, undefined),\n                    /*#__PURE__*/ (0,react_jsx_dev_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxDEV)(_barrel_optimize_names_Box_Button_List_ListItem_ListItemText_TextField_Typography_mui_material__WEBPACK_IMPORTED_MODULE_2__.Button, {\n                        onClick: handleSendMessage,\n                        variant: \"contained\",\n                        children: \"Send\"\n                    }, void 0, false, {\n                        fileName: \"/home/john/INLPT/Project_Medical-INLPT-WS2023/server/frontend/src/components/chatBox.tsx\",\n                        lineNumber: 131,\n                        columnNumber: 9\n                    }, undefined)\n                ]\n            }, void 0, true, {\n                fileName: \"/home/john/INLPT/Project_Medical-INLPT-WS2023/server/frontend/src/components/chatBox.tsx\",\n                lineNumber: 104,\n                columnNumber: 7\n            }, undefined)\n        ]\n    }, void 0, true, {\n        fileName: \"/home/john/INLPT/Project_Medical-INLPT-WS2023/server/frontend/src/components/chatBox.tsx\",\n        lineNumber: 57,\n        columnNumber: 5\n    }, undefined);\n};\n_s(ChatComponent, \"AcnH96AQ5vsGJs4IDoqJySc9Qg0=\");\n_c = ChatComponent;\n/* harmony default export */ __webpack_exports__[\"default\"] = (ChatComponent);\nvar _c;\n$RefreshReg$(_c, \"ChatComponent\");\n\n\n;\n    // Wrapped in an IIFE to avoid polluting the global scope\n    ;\n    (function () {\n        var _a, _b;\n        // Legacy CSS implementations will `eval` browser code in a Node.js context\n        // to extract CSS. For backwards compatibility, we need to check we're in a\n        // browser context before continuing.\n        if (typeof self !== 'undefined' &&\n            // AMP / No-JS mode does not inject these helpers:\n            '$RefreshHelpers$' in self) {\n            // @ts-ignore __webpack_module__ is global\n            var currentExports = module.exports;\n            // @ts-ignore __webpack_module__ is global\n            var prevSignature = (_b = (_a = module.hot.data) === null || _a === void 0 ? void 0 : _a.prevSignature) !== null && _b !== void 0 ? _b : null;\n            // This cannot happen in MainTemplate because the exports mismatch between\n            // templating and execution.\n            self.$RefreshHelpers$.registerExportsForReactRefresh(currentExports, module.id);\n            // A module can be accepted automatically based on its exports, e.g. when\n            // it is a Refresh Boundary.\n            if (self.$RefreshHelpers$.isReactRefreshBoundary(currentExports)) {\n                // Save the previous exports signature on update so we can compare the boundary\n                // signatures. We avoid saving exports themselves since it causes memory leaks (https://github.com/vercel/next.js/pull/53797)\n                module.hot.dispose(function (data) {\n                    data.prevSignature =\n                        self.$RefreshHelpers$.getRefreshBoundarySignature(currentExports);\n                });\n                // Unconditionally accept an update to this module, we'll check if it's\n                // still a Refresh Boundary later.\n                // @ts-ignore importMeta is replaced in the loader\n                module.hot.accept();\n                // This field is set when the previous version of this module was a\n                // Refresh Boundary, letting us know we need to check for invalidation or\n                // enqueue an update.\n                if (prevSignature !== null) {\n                    // A boundary can become ineligible if its exports are incompatible\n                    // with the previous exports.\n                    //\n                    // For example, if you add/remove/change exports, we'll want to\n                    // re-execute the importing modules, and force those components to\n                    // re-render. Similarly, if you convert a class component to a\n                    // function, we want to invalidate the boundary.\n                    if (self.$RefreshHelpers$.shouldInvalidateReactRefreshBoundary(prevSignature, self.$RefreshHelpers$.getRefreshBoundarySignature(currentExports))) {\n                        module.hot.invalidate();\n                    }\n                    else {\n                        self.$RefreshHelpers$.scheduleUpdate();\n                    }\n                }\n            }\n            else {\n                // Since we just executed the code for the module, it's possible that the\n                // new exports made it ineligible for being a boundary.\n                // We only care about the case when we were _previously_ a boundary,\n                // because we already accepted this update (accidental side effect).\n                var isNoLongerABoundary = prevSignature !== null;\n                if (isNoLongerABoundary) {\n                    module.hot.invalidate();\n                }\n            }\n        }\n    })();\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,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NEJBQ2pCOUMsaUJBQWlCSSxXQUFXeUQsTUFBTTs0QkFBQzs7Ozs7OztrQ0FFdEMsOERBQUNsRSxrSUFBTUE7d0JBQUNtRSxTQUFTOUM7d0JBQW1COEIsU0FBUTtrQ0FBWTs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBTWhFO0dBdEhNN0M7S0FBQUE7QUF3SE4sK0RBQWVBLGFBQWFBLEVBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9fTl9FLy4vc3JjL2NvbXBvbmVudHMvY2hhdEJveC50c3g/Y2Y4NSJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgUmVhY3QsIHsgdXNlU3RhdGUgfSBmcm9tIFwicmVhY3RcIjtcclxuaW1wb3J0IHtcclxuICBCb3gsXHJcbiAgVGV4dEZpZWxkLFxyXG4gIEJ1dHRvbixcclxuICBMaXN0LFxyXG4gIExpc3RJdGVtLFxyXG4gIExpc3RJdGVtVGV4dCxcclxuICBUeXBvZ3JhcGh5LFxyXG59IGZyb20gXCJAbXVpL21hdGVyaWFsXCI7XHJcblxyXG50eXBlIE1lc3NhZ2VUeXBlID0ge1xyXG4gIHRleHQ6IHN0cmluZztcclxuICB0eXBlOiBcInVzZXJcIiB8IFwiYXNzaXN0YW50XCI7XHJcbn07XHJcblxyXG5jb25zdCBNQVhfQ0hBUkFDVEVSUyA9IDQwMDA7XHJcblxyXG5jb25zdCBDaGF0Q29tcG9uZW50OiBSZWFjdC5GQyA9ICgpID0+IHtcclxuICBjb25zdCBbbWVzc2FnZXMsIHNldE1lc3NhZ2VzXSA9IHVzZVN0YXRlPE1lc3NhZ2VUeXBlW10+KFtdKTtcclxuICBjb25zdCBbbmV3TWVzc2FnZSwgc2V0TmV3TWVzc2FnZV0gPSB1c2VTdGF0ZTxzdHJpbmc+KFwiXCIpO1xyXG4gIGNvbnN0IFtkYXRhLCBzZXREYXRhXSA9IHVzZVN0YXRlPHN0cmluZz4oXCJcIik7XHJcblxyXG4gIGNvbnN0IHJlcXVlc3QgPSBuZXcgUmVxdWVzdChcImh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9nZXQtYW5zd2VyLWZyb20tbG9jYWxcIiwge1xyXG4gICAgbWV0aG9kOiBcIlBPU1RcIixcclxuICAgIGhlYWRlcnM6IHtcclxuICAgICAgXCJDb250ZW50LVR5cGVcIjogXCJhcHBsaWNhdGlvbi9qc29uXCIsXHJcbiAgICB9LFxyXG4gICAgYm9keTogSlNPTi5zdHJpbmdpZnkoe1xyXG4gICAgICBxdWVzdGlvbjogbmV3TWVzc2FnZSxcclxuICAgIH0pLFxyXG4gIH0pO1xyXG5cclxuICBhc3luYyBmdW5jdGlvbiBoYW5kbGVTZW5kTWVzc2FnZSgpIHtcclxuICAgIGNvbnNvbGUubG9nKG5ld01lc3NhZ2UpO1xyXG4gICAgc2V0TWVzc2FnZXMoWy4uLm1lc3NhZ2VzLCB7IHRleHQ6IG5ld01lc3NhZ2UsIHR5cGU6IFwidXNlclwiIH1dKTtcclxuICAgIHNldE5ld01lc3NhZ2UoXCJcIik7XHJcbiAgICB0cnkge1xyXG4gICAgICBjb25zdCByZXNwb25zZSA9IGF3YWl0IGZldGNoKHJlcXVlc3QpO1xyXG4gICAgICBjb25zdCBkYXRhID0gYXdhaXQgcmVzcG9uc2UuanNvbigpO1xyXG4gICAgICBjb25zb2xlLmxvZyhkYXRhKTtcclxuXHJcbiAgICAgIGlmIChyZXNwb25zZS5zdGF0dXMgPT09IDIwMCkge1xyXG4gICAgICAgIHNldE1lc3NhZ2VzKChwcmV2TWVzc2FnZXM6IGFueSkgPT4gW1xyXG4gICAgICAgICAgLi4ucHJldk1lc3NhZ2VzLFxyXG4gICAgICAgICAgeyB0ZXh0OiBkYXRhLCB0eXBlOiBcImFzc2lzdGFudFwiIH0sXHJcbiAgICAgICAgXSk7XHJcbiAgICAgIH0gZWxzZSB7XHJcbiAgICAgICAgY29uc29sZS5sb2coXCJTb21ldGhpbmcgd2VudCB3cm9uZ1wiKTtcclxuICAgICAgfVxyXG4gICAgfSBjYXRjaCAoZXJyb3IpIHtcclxuICAgICAgY29uc29sZS5sb2coZXJyb3IpO1xyXG4gICAgfVxyXG4gIH1cclxuXHJcbiAgcmV0dXJuIChcclxuICAgIDxCb3hcclxuICAgICAgc3g9e3tcclxuICAgICAgICBkaXNwbGF5OiBcImZsZXhcIixcclxuICAgICAgICBmbGV4RGlyZWN0aW9uOiBcImNvbHVtblwiLFxyXG4gICAgICAgIGhlaWdodDogXCI1MCVcIixcclxuICAgICAgICB3aWR0aDogXCI1MCVcIixcclxuICAgICAgICBwb3NpdGlvbjogXCJhYnNvbHV0ZVwiLFxyXG4gICAgICAgIHRvcDogXCI1MCVcIixcclxuICAgICAgICBsZWZ0OiBcIjUwJVwiLFxyXG4gICAgICAgIHRyYW5zZm9ybTogXCJ0cmFuc2xhdGUoLTUwJSwgLTUwJSlcIixcclxuICAgICAgICBib3JkZXI6IFwiMXB4IHNvbGlkIGdyYXlcIixcclxuICAgICAgICBib3JkZXJSYWRpdXM6IFwiMTBweFwiLFxyXG4gICAgICB9fVxyXG4gICAgPlxyXG4gICAgICA8Qm94IHN4PXt7IG92ZXJmbG93OiBcImF1dG9cIiwgZmxleEdyb3c6IDEgfX0+XHJcbiAgICAgICAgPExpc3Q+XHJcbiAgICAgICAgICB7bWVzc2FnZXMubWFwKChtZXNzYWdlOiBhbnksIGluZGV4OiBhbnkpID0+IChcclxuICAgICAgICAgICAgPExpc3RJdGVtXHJcbiAgICAgICAgICAgICAga2V5PXtpbmRleH1cclxuICAgICAgICAgICAgICBzeD17e1xyXG4gICAgICAgICAgICAgICAganVzdGlmeUNvbnRlbnQ6XHJcbiAgICAgICAgICAgICAgICAgIG1lc3NhZ2UudHlwZSA9PT0gXCJ1c2VyXCIgPyBcImZsZXgtZW5kXCIgOiBcImZsZXgtc3RhcnRcIixcclxuICAgICAgICAgICAgICB9fVxyXG4gICAgICAgICAgICA+XHJcbiAgICAgICAgICAgICAgPExpc3RJdGVtVGV4dFxyXG4gICAgICAgICAgICAgICAgc3g9e3tcclxuICAgICAgICAgICAgICAgICAgdGV4dEFsaWduOiBtZXNzYWdlLnR5cGUgPT09IFwidXNlclwiID8gXCJyaWdodFwiIDogXCJsZWZ0XCIsXHJcbiAgICAgICAgICAgICAgICB9fVxyXG4gICAgICAgICAgICAgICAgcHJpbWFyeT17XHJcbiAgICAgICAgICAgICAgICAgIDxUeXBvZ3JhcGh5XHJcbiAgICAgICAgICAgICAgICAgICAgdmFyaWFudD1cImJvZHkxXCJcclxuICAgICAgICAgICAgICAgICAgICBzeD17e1xyXG4gICAgICAgICAgICAgICAgICAgICAgYmFja2dyb3VuZENvbG9yOlxyXG4gICAgICAgICAgICAgICAgICAgICAgICBtZXNzYWdlLnR5cGUgPT09IFwidXNlclwiID8gXCJsaWdodGJsdWVcIiA6IFwiZ3JleVwiLFxyXG4gICAgICAgICAgICAgICAgICAgICAgcGFkZGluZzogXCI1cHhcIixcclxuICAgICAgICAgICAgICAgICAgICAgIGJvcmRlclJhZGl1czogXCIxMHB4XCIsXHJcbiAgICAgICAgICAgICAgICAgICAgICBkaXNwbGF5OiBcImlubGluZS1ibG9ja1wiLFxyXG4gICAgICAgICAgICAgICAgICAgIH19XHJcbiAgICAgICAgICAgICAgICAgID5cclxuICAgICAgICAgICAgICAgICAgICB7bWVzc2FnZS50ZXh0fVxyXG4gICAgICAgICAgICAgICAgICA8L1R5cG9ncmFwaHk+XHJcbiAgICAgICAgICAgICAgICB9XHJcbiAgICAgICAgICAgICAgLz5cclxuICAgICAgICAgICAgPC9MaXN0SXRlbT5cclxuICAgICAgICAgICkpfVxyXG4gICAgICAgIDwvTGlzdD5cclxuICAgICAgPC9Cb3g+XHJcbiAgICAgIDxCb3hcclxuICAgICAgICBzeD17e1xyXG4gICAgICAgICAgZGlzcGxheTogXCJmbGV4XCIsXHJcbiAgICAgICAgICBhbGlnbkl0ZW1zOiBcImNlbnRlclwiLFxyXG4gICAgICAgICAgcGFkZGluZzogMSxcclxuICAgICAgICAgIGJvcmRlclRvcDogXCIxcHggc29saWQgZ3JheVwiLFxyXG4gICAgICAgIH19XHJcbiAgICAgID5cclxuICAgICAgICA8VGV4dEZpZWxkXHJcbiAgICAgICAgICB2YWx1ZT17bmV3TWVzc2FnZX1cclxuICAgICAgICAgIG9uQ2hhbmdlPXsoZTogUmVhY3QuQ2hhbmdlRXZlbnQ8SFRNTElucHV0RWxlbWVudD4pID0+IHtcclxuICAgICAgICAgICAgc2V0TmV3TWVzc2FnZShlLnRhcmdldC52YWx1ZSk7XHJcbiAgICAgICAgICB9fVxyXG4gICAgICAgICAgdmFyaWFudD1cIm91dGxpbmVkXCJcclxuICAgICAgICAgIHBsYWNlaG9sZGVyPVwiV3JpdGUgYSBtZXNzYWdlXCJcclxuICAgICAgICAgIHN4PXt7XHJcbiAgICAgICAgICAgIGZsZXhHcm93OiAxLFxyXG4gICAgICAgICAgICBtYXJnaW5SaWdodDogMSxcclxuICAgICAgICAgICAgYm9yZGVyQ29sb3I6IFwicHJpbWFyeS5tYWluXCIsXHJcbiAgICAgICAgICAgIGJvcmRlcldpZHRoOiAyLFxyXG4gICAgICAgICAgICBib3JkZXJSYWRpdXM6IFwiNXB4XCIsXHJcbiAgICAgICAgICB9fVxyXG4gICAgICAgICAgaW5wdXRQcm9wcz17eyBtYXhMZW5ndGg6IE1BWF9DSEFSQUNURVJTIH19XHJcbiAgICAgICAgLz5cclxuICAgICAgICA8VHlwb2dyYXBoeSB2YXJpYW50PVwiYm9keTJcIj5cclxuICAgICAgICAgIHtNQVhfQ0hBUkFDVEVSUyAtIG5ld01lc3NhZ2UubGVuZ3RofS80MDAwXHJcbiAgICAgICAgPC9UeXBvZ3JhcGh5PlxyXG4gICAgICAgIDxCdXR0b24gb25DbGljaz17aGFuZGxlU2VuZE1lc3NhZ2V9IHZhcmlhbnQ9XCJjb250YWluZWRcIj5cclxuICAgICAgICAgIFNlbmRcclxuICAgICAgICA8L0J1dHRvbj5cclxuICAgICAgPC9Cb3g+XHJcbiAgICA8L0JveD5cclxuICApO1xyXG59O1xyXG5cclxuZXhwb3J0IGRlZmF1bHQgQ2hhdENvbXBvbmVudDtcclxuIl0sIm5hbWVzIjpbIlJlYWN0IiwidXNlU3RhdGUiLCJCb3giLCJUZXh0RmllbGQiLCJCdXR0b24iLCJMaXN0IiwiTGlzdEl0ZW0iLCJMaXN0SXRlbVRleHQiLCJUeXBvZ3JhcGh5IiwiTUFYX0NIQVJBQ1RFUlMiLCJDaGF0Q29tcG9uZW50IiwibWVzc2FnZXMiLCJzZXRNZXNzYWdlcyIsIm5ld01lc3NhZ2UiLCJzZXROZXdNZXNzYWdlIiwiZGF0YSIsInNldERhdGEiLCJyZXF1ZXN0IiwiUmVxdWVzdCIsIm1ldGhvZCIsImhlYWRlcnMiLCJib2R5IiwiSlNPTiIsInN0cmluZ2lmeSIsInF1ZXN0aW9uIiwiaGFuZGxlU2VuZE1lc3NhZ2UiLCJjb25zb2xlIiwibG9nIiwidGV4dCIsInR5cGUiLCJyZXNwb25zZSIsImZldGNoIiwianNvbiIsInN0YXR1cyIsInByZXZNZXNzYWdlcyIsImVycm9yIiwic3giLCJkaXNwbGF5IiwiZmxleERpcmVjdGlvbiIsImhlaWdodCIsIndpZHRoIiwicG9zaXRpb24iLCJ0b3AiLCJsZWZ0IiwidHJhbnNmb3JtIiwiYm9yZGVyIiwiYm9yZGVyUmFkaXVzIiwib3ZlcmZsb3ciLCJmbGV4R3JvdyIsIm1hcCIsIm1lc3NhZ2UiLCJpbmRleCIsImp1c3RpZnlDb250ZW50IiwidGV4dEFsaWduIiwicHJpbWFyeSIsInZhcmlhbnQiLCJiYWNrZ3JvdW5kQ29sb3IiLCJwYWRkaW5nIiwiYWxpZ25JdGVtcyIsImJvcmRlclRvcCIsInZhbHVlIiwib25DaGFuZ2UiLCJlIiwidGFyZ2V0IiwicGxhY2Vob2xkZXIiLCJtYXJnaW5SaWdodCIsImJvcmRlckNvbG9yIiwiYm9yZGVyV2lkdGgiLCJpbnB1dFByb3BzIiwibWF4TGVuZ3RoIiwibGVuZ3RoIiwib25DbGljayJdLCJzb3VyY2VSb290IjoiIn0=\n//# sourceURL=webpack-internal:///./src/components/chatBox.tsx\n"));

/***/ })

});