const Sequelize = require('sequelize');

module.exports = class Trend extends Sequelize.Model {
  static init(sequelize) {
    return super.init({
      
      Trend_Thumbnail_image : {
        type: Sequelize.STRING(2000),
        allowNull: true,
      },
      Trend_Title : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Trend_SubTitle : {
        type: Sequelize.STRING(100),
        allowNull: true,
      },
      Trend_text: {
        type: Sequelize.STRING(3000),
        allowNull: false,
      },


    }, {
      sequelize,
      timestamps: true,
      underscored: false,
      modelName: 'Trend',
      tableName: 'Trends',
      // 게시물은 실제 삭제하지 않고 deletedAt에 날짜를 넣다.
      // 수동 쿼리로 컬럼 생성 - ALTER TABLE posts ADD deletedAt DATETIME NULL;
      paranoid: true,
      charset: 'utf8mb4',  // 이모티콘 가능 
      collate: 'utf8mb4_general_ci',
    });
  }

  static associate(db) {
    db.Trend.belongsTo(db.User, {
      foreignKey: 'userId' // FK 컬럼명
    }); // 트랜드는 하나의 userId에 속한다       
  }
};
