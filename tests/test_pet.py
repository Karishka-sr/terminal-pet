"""Тесты основной механики питомца."""

from terminal_pet.pet import Pet, MAX_HUNGER, MAX_ENERGY, MOODS


def test_new_pet_has_defaults():
    pet = Pet()
    assert pet.name == "Yuki"
    assert pet.hunger == MAX_HUNGER
    assert pet.energy == MAX_ENERGY
    assert pet.happiness == 100
    assert pet.is_alive
    assert pet.mood == "happy"


def test_feed_restores_hunger():
    pet = Pet()
    pet.hunger = 30
    pet.feed(30)
    assert pet.hunger == 60


def test_feed_caps_at_max():
    pet = Pet()
    pet.hunger = 90
    pet.feed(50)
    assert pet.hunger == MAX_HUNGER


def test_feed_increments_counter_and_happiness():
    pet = Pet()
    pet.hunger = 10
    pet.feed(40)
    assert pet.times_fed == 1
    assert pet.happiness == 100  # уже максимум


def test_play_costs_energy_gains_happiness():
    pet = Pet()
    pet.play()
    assert pet.energy == MAX_ENERGY - 15
    assert pet.happiness == 100  # максимум
    assert pet.hunger == MAX_HUNGER - 5


def test_play_refuses_when_tired():
    pet = Pet()
    pet.energy = 10
    result = pet.play()
    assert "спать" in result
    assert pet.energy == 10


def test_play_refuses_when_starving():
    pet = Pet()
    pet.hunger = 10
    result = pet.play()
    assert "покорми" in result


def test_sleep_restores_energy():
    pet = Pet()
    pet.energy = 10
    pet.sleep()
    assert pet.energy == 60


def test_tick_decreases_hunger_and_age():
    pet = Pet()
    pet.tick()
    assert pet.age == 1
    assert pet.hunger == MAX_HUNGER - 3


def test_death_by_neglect():
    pet = Pet()
    pet.hunger = 0
    pet.happiness = 0
    result = pet.tick()
    assert result is not None
    assert not pet.is_alive
    assert pet.mood == "sad"


def test_dead_pet_wont_act():
    pet = Pet()
    pet.is_alive = False
    assert "не с нами" in (pet.feed(30) + pet.play() + pet.sleep())


def test_mood_hungry():
    pet = Pet()
    pet.hunger = 10
    pet.energy = 100
    pet._update_mood()
    assert pet.mood == "hungry"


def test_mood_asleep():
    pet = Pet()
    pet.energy = 10
    pet._update_mood()
    assert pet.mood == "asleep"


def test_mood_sad_when_unhappy():
    pet = Pet()
    pet.happiness = 10
    pet.hunger = 50
    pet.energy = 80
    pet._update_mood()
    assert pet.mood == "sad"


def test_all_moods_renderable():
    from terminal_pet.ascii import render

    for mood in MOODS:
        pet = Pet()
        pet.mood = mood
        art = render(pet)
        assert art  # не пусто


def test_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "pet.json"
    pet = Pet(name="Кексик")
    pet.feed(10)
    pet.tick()
    pet.tick()
    pet.save(path)

    restored = Pet.load(path)
    assert restored.name == pet.name
    assert restored.age == pet.age
    assert restored.hunger == pet.hunger
    assert restored.energy == pet.energy
    assert restored.happiness == pet.happiness
    assert restored.times_fed == pet.times_fed


def test_load_missing_file_returns_fresh_pet(tmp_path):
    pet = Pet.load(tmp_path / "nonexistent.json")
    assert pet.age == 0
    assert pet.is_alive