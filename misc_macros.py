

def define_env(env):

	@env.macro
	def hello_macro(test_text : str):
		print(f"running. test: <{test_text}>")
		return f"macro <{test_text}>"

	@env.macro
	def hello_nav(test_text : str):
		print(f"running. test of nav.")
		return f"macro <{env.conf['nav']}>"
	
	