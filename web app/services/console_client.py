from views_controller import views_controller

def main():
    # Get the number of views for a particular use
    controller = views_controller()
    views = controller.get_contents_viewed_by_userid("1007")
    for view in views:
        print(view)



if __name__ == "__main__":
    main()