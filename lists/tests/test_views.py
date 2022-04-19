from django.test import TestCase
from django.utils.html import escape
from lists.models import Item, List
from lists.forms import (
    EMPTY_ITEM_ERROR,
    DUPLICATE_ITEM_ERROR,
    ExistingListItemForm,
    ItemForm,
)
from unittest import skip


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_home_page_uses_item_form(self):
        response = self.client.get("/")
        self.assertIs(response.context["form"], ItemForm)


class NewListTest(TestCase):
    def test_redirects_after_post(self):
        response = self.client.post("/lists/new", data={"text": "A new list item"})
        new_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{new_list.id}/")

    def test_can_save_a_post_request(self):
        self.client.post("/lists/new", data={"text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post("/lists/new", data={"text": ""})
        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertIsInstance(response.context["form"], ItemForm)

    def test_invalid_list_items_arent_saved(self):
        self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_display_only_items_for_that_list(self):
        list_ = List.objects.create()
        Item.objects.create(text="itemey 1", list=list_)
        Item.objects.create(text="itemey 2", list=list_)
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        other = List.objects.create()
        Item.objects.create(text="other item 1", list=other)
        Item.objects.create(text="other item 2", list=other)
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "other item 1")
        self.assertNotContains(response, "other item 2")

    def test_passes_correct_list_to_template(self):
        other = List.objects.create()
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertEqual(response.context["list"], list_)

    def test_can_save_a_post_request_to_an_existing_list(self):
        other = List.objects.create()
        list_ = List.objects.create()
        text = "A new item for an existing list"
        self.client.post(f"/lists/{list_.id}/", data={"text": text})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, text)
        self.assertEqual(new_item.list, list_)

    def test_post_redirects_to_list_view(self):
        other = List.objects.create()
        list_ = List.objects.create()
        text = "A new item for an existing list"
        response = self.client.post(f"/lists/{list_.id}/", data={"text": text})
        self.assertRedirects(response, f"/lists/{list_.id}/")

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(f"/lists/{list_.id}/", data={"text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list.html")
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(f"/lists/{list_.id}/", data={"text": ""})

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list.html")

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text="textey")
        response = self.client.post(f"/lists/{list1.id}/", data={"text": "textey"})
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, "list.html")
        self.assertEqual(Item.objects.all().count(), 1)

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertIsInstance(response.context["form"], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context["form"], ExistingListItemForm)
