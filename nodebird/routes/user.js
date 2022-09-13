const express = require('express');  //라우터를 통해 요청을 받는 라이브러리

const { isLoggedIn } = require('./middlewares');
const User = require('../models/user');

const router = express.Router(); // 이 변수는 익스프레스 라우터를 쓴다

router.post('/:id/follow', isLoggedIn, async (req, res, next) => {  // 이미 app.js에서 /user가 붙어서 왓기때문에 
  try {                                                             // 여기 주소세너는 /user가 빠지고 그 이후부터 기입 
    const user = await User.findOne({ where: { id: req.user.id } });
    if (user) {
      await user.addFollowing(parseInt(req.params.id, 10));
      res.send('success');
    } else {
      res.status(404).send('no user');
    }
  } catch (error) {
    console.error(error);
    next(error);
  }
});

/**
 * nick(이름) 수정 라우터 
 */
 router.post('/nickupdate', isLoggedIn, async (req, res) => {
  // 닉 내용
  const nick = req.body.nick;
  const userId = req.session.passport.user;

  // 닉을 수정한다 
  await User.update({
    nick: nick
  },
  {
    where: {
      id: userId
    }
  }
  );

  // 수정 완료시 메인화면으로 이동시킨다.
  res.sendStatus(200);
});


module.exports = router;
