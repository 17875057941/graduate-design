import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const Recommend = (resolve) => {
  import('components/recommend/recommend').then((module) => {
    resolve(module)
  })
}

const Singer = (resolve) => {
  import('components/singer/singer').then((module) => {
    resolve(module)
  })
}

const Rank = (resolve) => {
  import('components/rank/rank').then((module) => {
    resolve(module)
  })
}

const Search = (resolve) => {
  import('components/search/search').then((module) => {
    resolve(module)
  })
}

const SingerDetail = (resolve) => {
  import('components/singer-detail/singer-detail').then((module) => {
    resolve(module)
  })
}

const Disc = (resolve) => {
  import('components/disc/disc').then((module) => {
    resolve(module)
  })
}

const TopList = (resolve) => {
  import('components/top-list/top-list').then((module) => {
    resolve(module)
  })
}

const UserCenter = (resolve) => {
  import('components/user-center/user-center').then((module) => {
    resolve(module)
  })
}

const Home = (resolve) => {
  import('components/home/home').then((module) => {
    resolve(module)
  })
}

const Index = (resolve) => {
  import('components/index/index').then((module) => {
    resolve(module)
  })
}

const Login = (resolve) => {
  import('components/login/login').then((module) => {
    resolve(module)
  })
}

const Register = (resolve) => {
  import('components/register/register').then((module) => {
    resolve(module)
  })
}

const Hobby = (resolve) => {
  import('components/hobby/hobby').then((module) => {
    resolve(module)
  })
}
export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/home',
      component: Home
    },
    {
      path: '/login',
      component: Login
    },
    {
      path: '/register',
      component: Register
    },
    {
      path: '/index',
      component: Index,
      children: [
        {
          path: '/recommend',
          component: Recommend,
          children: [
            {
              path: ':id',
              component: Disc
            }
          ]
        },
        {
          path: '/singer',
          component: Singer,
          children: [
            {
              path: ':id',
              component: SingerDetail
            }
          ]
        },
        {
          path: '/rank',
          component: Rank,
          children: [
            {
              path: ':id',
              component: TopList
            }
          ]
        },
        {
          path: '/search',
          component: Search,
          children: [
            {
              path: ':id',
              component: SingerDetail
            }
          ]
        },
        {
          path: '/user',
          component: UserCenter
        }
      ]
    },
    {
      path: '/hobby',
      component: Hobby
    }
  ]
})
