from typing import List

maps: List[str] = []

map_1: str = """
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🌊🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊🌊
⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🌊🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
🌴⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨
⬜⬜🌴⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜🌴
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊🌊
"""

maps.append(map_1)

map_2: str = """
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🌊🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊🌊
⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🌊🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
🌴⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨
⬜⬜🌴⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜🌴
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬛⬜⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
"""

maps.append(map_2)

map_3: str = """
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
🌴⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊
⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜🌴
⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛🟨⬜⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜🌴
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊
⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
"""

maps.append(map_3)

map_4: str = """
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨
🟨🟨🟨⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🌊🌊🌊
🟨🟨🟨⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊
🟨🟨🟨⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛🟨⬜⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜🌴
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊
⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
"""

maps.append(map_4)

map_5: str = """
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🟨🟨🟨🟨🟨🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🟨🌴🌴🌴🟨🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🟨🌴🌴🌴🟨🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🟨🟨🟨🟨🟨🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬛🟨🟨🟨⬛🟨🟨🟨
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬛🟨🟨⬛⬛⬛🟨🟨
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬛⬛🟨🟨⬛⬛⬛🟨🟨
🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬛⬛⬛⬛⬛⬛⬛⬛🟨🟨
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬛⬜🟨⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜🌴
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊
⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🌊🌊
"""

maps.append(map_5)

map_6: str = """
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🟨🟨🟨🟨🟨🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🟨🌴🌴🌴🟨🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🟨🌴🌴🌴🟨🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🟨🟨🟨🟨🟨🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬛🟨🟨🟨⬛🟨🟨🟨
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬛⬛⬛⬛⬛⬛🟨🟨
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬛⬛⬛⬛⬛⬛⬛🟨🟨
🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛🟨
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬛⬛⬛⬛
⬜⬜⬜⬜⬜🟨🟨🟨🟨🟨⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛
⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜🌴⬜⬜⬜⬛⬛⬛⬛
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜🌴⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛
⬛⬛⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🌴⬛⬛
⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜
⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜
⬛⬛⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬛⬛⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬛⬛⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜🟨🟨⬛⬛⬛
🌴🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬛⬛⬛⬛⬛🟨🟨⬛⬛⬛
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨⬛⬛⬛
"""

maps.append(map_6)

map_7: str = """
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜🌴⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜🌴⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
🌴⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬛⬛⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜
⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜
⬛⬛⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬛⬛⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜🌴⬜
⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
"""

maps.append(map_7)

map_8: str = """
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨
⬜⬜⬜⬜⬜⬜⬛⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨
⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜⬜🟨
⬜⬜⬜⬜⬛⬜⬛⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜🟨
⬜⬜⬜⬛⬜⬜⬜⬛⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜🟨
⬜⬜⬛⬜⬛⬜⬜⬜⬛⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜🟨
⬜⬛⬜⬜⬜⬛⬜⬜⬜⬛⬜⬜⬜⬜⬛⬜⬜⬜⬜🟨
⬜🌴⬜⬜⬜🌴⬜⬜⬜⬜⬛⬜⬜⬜⬜⬛⬜🌴⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬛⬜⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬛⬜🟨
⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬛🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜🌴⬜⬜🌴⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜🟨
🌴⬜⬜⬜⬜⬜⬜🌴⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨
⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜🌴⬜
⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
"""

maps.append(map_8)

map_9: str = """
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌊🌊🌊🌊
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🌊🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬜🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬛⬛🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬛🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
⬜⬜⬜⬜⬜⬛🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
⬜⬜⬜⬜⬜⬜🌊⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜🟨🌊
⬜⬜⬜⬜⬜⬜⬜🌊⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜🟨
⬜⬜🟨🟨⬛🌊🌊🌊🌊🌊⬜⬜⬜⬛⬜⬜⬜⬜⬜🟨
⬜🟨🟨🌊🌊⬛🌊🌊🌊⬛⬜⬜⬜⬜⬛⬜⬜⬜⬜🟨
⬜🟨🟨🌊🌊🌴🌊🌊🌊🌊⬛⬜⬜⬜⬜⬛⬜🌴⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬛⬜⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬛⬜🟨
⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜🟨🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜🌴⬜⬜🌴⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜🟨
🌴⬜⬜⬜⬜⬜⬜🌴⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨
⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜🌊🌊🌊🌊🌊⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜🌊🌊🌊🌊🌊⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜🌴⬜
⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌊🌊🌊🌊🌊⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
"""

maps.append(map_9)

map_10: str = """
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌊🌊🌊🌊
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🌊🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬜🌊🌊🌊🌊🌊🌴🌴🌴🌴🌴🌴🌴
⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬛⬛🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬛🌊🌊🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴
⬜⬜⬜⬜⬜⬛🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
⬜⬜⬜⬜⬜⬜🌊⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜🟨🌊
⬜⬜⬜⬜⬜⬜⬜🌊⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜🟨
⬜⬜🟨🌊⬛🌊🌊🌊🌊🌊⬜⬜⬜🌴⬜⬜⬜⬜⬜🟨
⬜🟨🌊🌊🌊⬛🌊🌊🌊⬛⬜⬜⬜⬜🌴⬜⬜⬜⬜🟨
⬜🟨🌊🌊🌊🌴🌊🌊🌊🌊⬛⬜⬜⬜⬜🌴⬜🟨⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜🟨🌴
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜🟨🌴
🌴🌴🌴🌴🌴⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜🟨🌴
⬜⬜🌴🌴⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜🌴⬜⬜🟨⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜🟨
🟨⬜⬜⬜⬜⬜⬜🌴⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🟨⬜⬜⬜⬜⬜⬜⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨⬜⬜⬜⬜⬜⬜⬜⬜🟨
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬜⬜🌴⬜⬜⬜⬜⬜🟨
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬜⬜⬜⬜⬜⬜⬜⬜
🟨🟨🟨🟨🟨🌊🌊🌊🌊🌊⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜
🌊🌊🌊⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜🌴
🌊🌊⬛⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴
🌊⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴🌴🌴🌴🌴⬜🟨⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
"""

maps.append(map_10)

map_11: str = """
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🟨
🌴🌴🌴🟨🟨🟨🟨⬜⬜⬜⬜⬜🟨⬜⬜⬜⬜⬜🟨🟨
⬜⬜⬜⬜⬜⬜⬜⬜🌊🌊🌊🌊🌊⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬛⬛🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬜⬛⬛🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
⬜⬜⬜⬜⬜⬜⬛🌊🌊🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴
⬜⬜⬜⬜⬜⬛🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
⬜⬜⬜⬜⬜⬜🌊⬜⬜⬜⬛⬜⬜⬜⬜⬜⬜⬜🟨🌊
⬜⬜⬜⬜⬜⬜⬜🌊⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜🟨
⬜⬜⬛🌊⬛🌊🌊🌊🌊🌊⬜⬜⬜🌴⬜⬜⬜⬜⬜🟨
⬜⬛🌊🌊🌊⬛🌊🌊🌊⬛⬜⬜⬜⬜🌴⬜⬜⬜⬜🟨
⬜🌴🌊🌊🌊🌴🌊🌊🌊🌊⬛⬜⬜⬜⬜🌴⬜🟨⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜🟨🌴
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🌴
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨🌴
⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜🟨⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨
🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴🌴🌴🌴🌴🌴🌴🌴
⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🟨⬜⬜⬜⬜⬜⬜⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨⬜⬜⬜⬜⬜⬜⬜⬜🟨
🌴🌴🌴🌴🌴🟨🟨🟨🟨🟨🟨⬜⬜🌴⬜⬜⬜⬜⬜🟨
🌴🌴🌴🌴🌴🟨🟨🟨🟨🟨🟨🟨⬜⬜⬜⬜⬜🌴🌴🌴
🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴⬜⬜⬜⬜⬜🌴🌴🌴🌴
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜
🌊🌊🌊🌴🌴🌴⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜🌴
🌊🌊⬛⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴
🌊⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴🌴🌴🌴🌴⬜🟨⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
"""

maps.append(map_11)

map_12: str = """
🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴
🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴
🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨
🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🌴🌴🌴🌴🌴🌴🌴🌴
🌴🌴🌴🌴🌴🌴🌴🟨🟨🟨🟨🟨🌴🌴🌴🌴🌴🌴🌴🌴
🌴🌴🌴🌴🌴🌴🌴🟨🟨🟨🟨🟨🌴🌴🌴🌴🌴🌴🌴🌴
⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🟨🟨🌴⬜⬜⬜⬜⬜⬜🟨
⬜⬜🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬜🌴⬜⬜⬜⬜⬜🟨
⬜🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬜⬜🌴⬜⬜⬜⬜🟨
⬜🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨⬜⬜⬜⬜⬜⬜⬜⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜🟨🌴
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴🌴🌴🌴🌴🌴🌴🌴
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴🌴🌴🌴🌴🌴🌴🌴
⬜⬜⬜🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬜⬜🌴⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨
🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜🟨🟨🟨🟨⬜⬜⬜⬜⬜⬜⬜🟨
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🟨⬜⬜⬜⬜⬜⬜⬜⬜🟨
🌴🌴🌴🌴🌴🟨🟨🟨🟨🟨🟨⬜⬜🌴⬜⬜⬜⬜⬜🟨
🌴🌴🌴🌴🌴🟨🟨🟨🟨🟨🟨🟨⬜⬜⬜⬜⬜⬜⬜⬜
🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌴⬜⬜⬜⬜⬜⬜⬜⬜⬜
🌊🌊🌊🌴🌴🌴⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
"""

maps.append(map_12)

map_13: str = """
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊🌊⬛⬛⬛⬛🌊🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊🌊🌊🌊⬛⬛🟨🟨🟨⬛🌊🌊🌊🌊🌊🌊🌊
🌊🌊🌊🌊⬛⬛⬛⬛🟨🟨🟨🟨⬜⬛⬛⬛🌊🌊🌊🌊
🌊🌊🌊🌊⬛🟨🟨🟨🟨🟨🟨🟨⬜⬜🌴⬛🌊🌊🌊🌊
🌊🌊🌊🌊⬛🟨🟨🟨🟨🟨🟨⬜⬜⬜⬜⬛🌊🌊🌊🌊
🌊🌊🌊🌊⬛⬜⬜⬜⬜⬜⬜🌴⬜⬜⬜⬛🌊🌊🌊🌊
🌊🌊🌊⬛⬛⬜⬜⬜⬜⬜⬜⬜🌴🌴🌴⬛🌊🌊🌊🌊
🌊🌊🌊🌊⬛⬜⬜⬜⬜⬜⬜⬜🌴🌴🌴⬛🌊🌊🌊🌊
🌊🌊🌊🌊⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴⬛🌊🌊🌊🌊
🌊🌊🌊🌊⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🌊🌊🌊🌊
🌊🌊🌊🌊⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛🌊🌊🌊
🌊🌊🌊🌊⬛⬜⬜⬜🟨🟨🟨🟨⬜⬜⬜⬜⬜⬛🌊🌊
🌊🌊🌊🌊⬛⬜⬜⬜⬜⬜🟨⬜⬜⬜⬜⬜⬜⬜⬛🌊
🌊🌊🌊🌊⬛🟨🟨🟨🟨🟨🟨⬜⬜🟨⬜⬜⬜⬜⬜⬛
🌊🌊🌊🌊⬛⬛⬛⬛⬛⬛⬛🟨⬜⬜⬜⬜⬜⬜⬜⬜
🌊🌊🌊🌊🌴🌴🌴🌴🌴🌴🌴⬛⬜⬜⬜⬜⬜⬜⬜⬜
🌊🌊🌊🌊🌊🌊🌊🌊🌊🌊🌴⬛⬜⬜⬜⬜⬜⬜⬜⬜
🌊🌊🌊⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜🌴
⬛⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜🌴
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
"""

maps.append(map_13)