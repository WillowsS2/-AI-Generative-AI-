import openai
# pip install openai 
# pip install --upgrade openai

# OpenAI API 키 설정
openai.api_key = 'YOUR_API_KEY'  # 실제 API 키로 변경해주세요

def generate_creative_outline(topic, num_sections):
    # GPT를 활용하여 창의적인 목차 생성
    prompt = f"현재 생성중인 목차: {topic}. Include {num_sections} sections about:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )
    creative_outlines = response.choices[0].text.strip().split("\n")
    return creative_outlines

def modify_outline(outlines):
    # GPT를 활용하여 목차 수정
    modified_outlines = outlines.copy()

    print("\n현재 생성중인 목차:")
    for i, outline in enumerate(modified_outlines, 1):
        print(f"{i}. {outline}")

    # 사용자에게 수정할 내용 입력 받기
    user_modifications = input(f"\n{modification_prompt}\n")

    # GPT를 통해 사용자의 입력을 반영하여 목차 수정
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{modification_prompt}\nUser Modifications: {user_modifications}",
        max_tokens=500,
        temperature=0.7
    )
    modified_outlines = response.choices[0].text.strip().split("\n")

    return modified_outlines

def save_to_file(title, sections):
    # 최종 목차를 파일로 저장
    with open(f"{title}.txt", "w", encoding="utf-8") as file:
        file.write(f"{title}\n\n")
        for section in sections:
            file.write(f"{section}\n\n")
    print(f"\n\"{title}.txt\" 파일로 목차가 저장되었습니다.")

if __name__ == "__main__":
    while True:
        # 사용자로부터 주제 입력 받기
        user_topic = input("원하는 주제를 입력하세요: ")

        # 생성할 목차 항목 개수 입력 받기
        num_sections = int(input("생성할 목차 항목 개수를 입력하세요 (8-10): "))

        # 창의적인 목차 생성
        creative_outlines = generate_creative_outline(user_topic, num_sections)

        # 목차 수정
        modified_outlines = modify_outline(creative_outlines)

        while True:
            # 현재 수정된 목차 출력
            print("\n생성중인 목차:")
            for i, outline in enumerate(modified_outlines or [], 1):
                print(f"{i}. {outline}")

            # 목차 수정 여부 확인
            modify_option = input("\n목차를 수정하시겠습니까? (y/n): ")
            if modify_option.lower() == 'y':
                # 수정할 목차 항목의 번호 입력 받기
                modify_index = int(input("수정할 목차 항목의 번호를 입력하세요 (1부터 시작, 0: 종료): "))
                if 1 <= modify_index <= len(modified_outlines):
                    # 선택한 목차 수정
                    new_section = input(f"새로운 내용으로 목차 {modify_index}을 입력하세요: ")
                    if new_section:
                        # 새로운 내용이 입력되었다면 수정
                        modified_outlines[modify_index - 1] = new_section
                        print(f"목차 {modify_index}이(가) 성공적으로 수정되었습니다.")
                    else:
                        print("내용이 입력되지 않아 수정되지 않았습니다.")
                elif modify_index == 0:
                    break  # 수정 종료
                else:
                    print("올바른 목차 번호를 입력하세요.")
            else:
                break  # 목차 수정 종료

        # 추가 목차 생성하지 않을 경우 파일로 저장 여부 물어보기
        print("\n목차 생성을 완료하였습니다.")
        save_option = input("\n생성한 목차를 파일로 저장하시겠습니까? (y/n): ")
        if save_option.lower() == 'y':
            # 최종 목차를 파일로 저장
            save_to_file(user_topic, modified_outlines)

        new_topic_option = input("\n추가적인 목차 생성이 필요하십니까? (y/n): ")
        if new_topic_option.lower() != 'y':
            break
