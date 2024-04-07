import random

def main():
    hands = ['1.グー', '2.チョキ', '3.パー']
    rules = {
        ('グー', 'チョキ'): '勝ち',
        ('チョキ', 'パー'): '勝ち',
        ('パー', 'グー'): '勝ち',
        ('グー', 'パー'): '負け',
        ('チョキ', 'グー'): '負け',
        ('パー', 'チョキ'): '負け',
        ('グー', 'グー'): 'あいこ',
        ('チョキ', 'チョキ'): 'あいこ',
        ('パー', 'パー'): 'あいこ',
    }

    print('じゃんけんをしよう！')
    user_hand = input('グー、チョキ、パーのどれを出す？: ')
    if user_hand not in hands:
        print('グー、チョキ、パーのいずれかを入力してください。')
        return

    comp_hand = random.choice(hands)
    print(f'あなたは{user_hand}、コンピュータは{comp_hand}を出しました。')

    result = rules[(user_hand, comp_hand)]
    print(f'結果は{result}です！')

if __name__ == '__main__':
    main()
