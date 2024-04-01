import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import ProjectMain from './views/Project_main.vue'
import EnvManage from "./views/EnvManage.vue"
import ApiManage from "./views/ApiManage.vue"
import UserDetail from "@/views/UserDetail.vue";
import PublicNotice from "@/views/PublicNotice.vue";
import UserManage from "@/views/UserManage.vue";
import ProjectCase from "@/views/ProjectCase.vue";
import TaskManage from "@/views/TaskManage.vue";
import ReportTask from "@/views/TaskReport.vue";
import ReportTestcase from "@/views/ReportTestcase.vue";
import Login from '@/views/Login.vue'

import TaskForm from "@/components/TaskForm.vue";
import DebugReportCaseList from "@/components/DubugReportCaseList.vue"
import ApiEdit from "@/components/ApiEdit.vue";
import PracticeManage from "@/views/PracticeManage.vue";
import ProjectVersionMain from "@/views/ProjectVersionNav.vue";
import HomeNav from "@/views/HomeNav.vue";

import ProjectVersionManage from "@/views/ProjectVersionManage.vue";
import VersionParams from "@/components/VersionParams.vue";
import VersionCaseList from './views/VersionCaseList.vue'
import VersionReport from './views/ReportManage.vue'

Vue.use(Router)

export default new Router({
    routes: [
        // {
        //     path: '/',
        //     name: 'home',
        //     component: Home
        // },
        {
            path: '/home',
            name: 'home',
            component: HomeNav,
            children: [
                {
                    path: '/project_main',
                    name: 'project_main',
                    component: ProjectMain,
                },
                {
                    path: '/version_manage',
                    name: 'version_manage',
                    component: ProjectVersionManage
                },
                {
                    path: '/practice',
                    name: 'practice',
                    component: PracticeManage,
                    meta: {
                        title: '练习数据'
                    },
                },
                {
                    path: '/task_manage',
                    name: 'task_manage',
                    component: TaskManage
                },
                {
                    path: '/api_manage',
                    name: 'api_manage',
                    component: ApiManage
                },
            ],
            meta:{
                title: '首页',
            }
        },
        {
            path: '/login',
            name: 'login',
            component: Login,
            meta:{
                title: '登录',
            }
        },
        {
            path: '/report_testcase',
            name: 'report_testcase',
            component: ReportTestcase
        },
        {
            path: '/task_form',
            name: 'task_form',
            component: TaskForm
        },
        {
            path: '/case_detail',
            name: 'case_detail',
            component: ProjectCase
        },
        {
            path: '/env_manage',
            name: 'env_manage',
            component: EnvManage
        },
        {
            path: '/api_edit',
            name: 'api_edit',
            component: ApiEdit
        },
        {
            path: '/user_detail',
            name: 'user_detail',
            component: UserDetail
        },
        {
            path: '/public_notice',
            name: 'public_notice',
            component: PublicNotice
        },
        {
            path: '/user_manage',
            name: 'user_manage',
            component: UserManage
        },
        {
            path: '/debug_report',
            name: 'debug_report',
            component: DebugReportCaseList
        },
        {
            path: '/project_version_nav',
            name: 'project_version_nav',
            redirect:'/version_case',
            component: ProjectVersionMain,
            children: [
                {
                    path: '/version_case',
                    name: 'version_case_list',
                    component: VersionCaseList
                },
                {
                    path: '/version_params',
                    name: 'version_params',
                    component: VersionParams,
                },
                {
                    path: '/version_task',
                    name: 'version_task',
                    component: TaskManage
                },
                {
                    path: '/version_report',
                    name:'version_report',
                    component:VersionReport,
                },
            ],
            meta: {
                title: '项目版本'
            },

        },
        // {
        //   path: '/about',
        //   name: 'about',
        //   // route level code-splitting
        //   // this generates a separate chunk (about.[hash].js) for this route
        //   // which is lazy-loaded when the route is visited.
        //   component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
        // }
    ]
})
