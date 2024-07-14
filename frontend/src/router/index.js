import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
    {
  path: '/',
  name: 'index',
      component: () => import(/* webpackChunkName: "about" */ '../views/index'),
      children: [
        {
          path: '/courseCenter',
          name: 'courseCenter',
          component: () => import(/* webpackChunkName: "about" */ '../views/course/courseCenter'),
          meta: {
            // title: '选课中心'
          }
        },
        {
          path: '/about',
          name: 'about',
          component: () => import(/* webpackChunkName: "about" */ '../components/About'),
          meta: {
            // title: '关于我们'
          }
        },
        {
          path: '/login',
          name: 'login',
          component: () => import(/* webpackChunkName: "about" */ '../components/user/login'),
          meta: {
            title: '用户登录'
          }
        },
        {
          path: '/studentInfo',
          name: 'studentInfo',
          meta: {
            requireAuth: true,  // 添加该字段，表示进入这个路由是需要登录的
            // title: '个人信息'
          },
          component: () => import(/* webpackChunkName: "about" */ '../components/user/userInfo'),

        },
        {
          path: '/studentCourse',
          name: 'studentCourse',
          meta: {
            requireAuth: true,  // 添加该字段，表示进入这个路由是需要登录的
            // title: '我的课程'
          },
          component: () => import(/* webpackChunkName: "about" */ '../views/student/studentCourse')
        }

        ],
      meta: {
          // title: '龙兴启智智教平台'
      }

  },
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "about" */ '../components/user/login'),
    meta: {
      title: '用户登录'
    }
  },
  {
    path: '/teacherHome',
    name: 'teacherHome',
    meta: {
      requireAuth: true,  // 添加该字段，表示进入这个路由是需要登录的
      // title: '龙兴启智智教平台'
    },
    children: [
      {
        path: '/teacherInfo',
        name: 'teacherInfo',
        meta: {
          requireAuth: true,  // 添加该字段，表示进入这个路由是需要登录的
          // title: '个人信息'
        },
        component: () => import(/* webpackChunkName: "about" */ '../components/user/userInfo')
      },
      {
        path: '/chosenCourses',
        name: 'chosenCourses',
        component: () => import(/* webpackChunkName: "about" */ '../views/teacher/chosenCourses'),
        meta: {
          // title: '学生选课管理'
        }
      },
      {
        path: '/teacherCourse',
        name: 'teacherCourse',
        component: () => import(/* webpackChunkName: "about" */ '../views/teacher/myCourses'),
        meta: {
          // title: '开课课程管理'
        }

      },
      {
        path: '/autoScoring',
        name: 'autoScoring',
        component: () => import(/* webpackChunkName: "about" */ '../components/AutoScoring2'),
        meta: {
          // title: '自动评分'
        }
      }
        ],
    component: () => import(/* webpackChunkName: "about" */ '@/views/teacher/teacherHome')
  },
  {
    path: '/adminHome',
    name: 'adminHome',
    meta: {
      requireAuth: true,  // 添加该字段，表示进入这个路由是需要登录的
    },
    component: () => import(/* webpackChunkName: "about" */ '@/views/admin/adminHome')
  },
  {
    path: '/courseDetail/:courseName',
    name: 'courseDetail',
    meta: {
      requireAuth: true,  // 添加该字段，表示进入这个路由是需要登录的
      // title: '课程详情'
    },
    component: () => import(/* webpackChunkName: "about" */ '@/views/course/courseDetail'),
    props: true, // 添加这一行，以便将路由参数传递给组件
  },
    {
      path: '/courseVideo/:courseName',
      name: 'courseVideo',
      component: () => import(/* webpackChunkName: "about" */ '../components/courseVideo'),
      meta: {
        // title: '课程视频'
      }
    },

]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach(async(to) => {
  if (to.meta.title) {
    document.title = to.meta.title
  } else {
    document.title = '龙兴启智智教平台' //此处写默认的title
  }
})

export default router
