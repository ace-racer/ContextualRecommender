from views_controller import views_controller

def main():
    #Get the number of views for a particular use
    controller = views_controller()
    controller.getContentsViewedByUserId("1007")


if __name__ == "__main__":
    main()