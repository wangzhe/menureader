import datetime
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base, db_session
from date import format_date

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)
    eng_name = Column(String(64), nullable=False)
    chin_name = Column(String(64), nullable=False)
    pinyin = Column(String(64), nullable=True)
    desc = Column(String(64), nullable=True)

    def get_json(self):
        data = {
            'dish': [
                {'Chinese': self.chin_name},
                {'English': self.eng_name},
            ]
        }

        if self.desc:
            data['dish'].append({'description': self.desc})

        if self.pinyin:
            data['pinyin'].append({'pinyin': self.pinyin})

        if self.reviews:
            reviews = [{review.user.username: "%s (%s)" % (review.text, format_date(review.date))} for review in self.reviews]
            data['reviews'] = reviews

        if self.dish_tags:
            tags_dict = {}
            for dish_tag in self.dish_tags:
                name = dish_tag.tag.name
                if tags_dict.get(name):
                    tags_dict[name] += 1
                else:
                    tags_dict[name] = 1

            tags = [{name: count} for name, count in tags_dict.iteritems()]
            data['tags'] = tags

        return data

    @staticmethod
    def get_dish_by_id(id):
        dish = db_session.query(Dish).get(id)
        return dish

    @staticmethod
    def find_match(word):
        return db_session.query(Dish).filter_by(chin_name=word).first()

    @staticmethod
    def find_similar(word):
        results = []
        word_list = []
        for char in word:
            word_list.append(char)

        for i in range(len(word)):
            temp = word_list[i]
            word_list[i] = '%'
            new_word = ''.join(word_list)

            similar = db_session.query(Dish).filter(Dish.chin_name.like(new_word)).all()
            results.extend(similar)
            word_list[i] = temp

        return results

    @staticmethod
    def get_all_dishes():
        dish_names = []
        dishes = db_session.query(Dish).all()
        for dish in dishes:
            dish_names.append(dish.chin_name)
        return dish_names



