from micoto import GUI

def main():
    """Main function"""
    try:
        GUI(admin=True)
        """Opens micoto in admin mode"""
    except:
        print("Can not open micoto app")
        """Writes console text"""

if __name__ == '__main__':
    """Opens micoto app in administrator mode"""
    main()