
window.onload = function()
{
	yearsList = [2022]; //include year 2022 in the list
	createPostForm = document.getElementById("createPostForm");
	resetForm(createPostForm);

  //create filter and fill it with year values from localStorage
	dropDownList = fillFilter();
	dropDownList.addEventListener("change", createPostDisplay);

	createPostDisplay(); //display posts from year 2022

	createPostForm.addEventListener("submit", (event) =>
	{
		event.preventDefault();
		if (Object.prototype.hasOwnProperty.call(localStorage,"posts") == false)
      localStorage.setItem("posts", JSON.stringify([])); //create empty list if there are no posts
		let newPost =
    {
      name: document.getElementById("name").value,
      date: document.getElementById("datePicker").value,
      url: document.getElementById("url").value,
      comment: document.getElementById("comment").value
    };

    //data validation below
		if(Date.parse(newPost.date) > Date.parse(new Date()))
			alert("Post cannot be dated in the future.");
		else if(newPost.name == "" || newPost.date == "" || newPost.url == "" || newPost.comment == "")
			alert("All fields are required.");
		else if(!newPost.name.includes(" "))
			alert("Please input both name and surname.");
		else
			doesImageLoad(newPost.url).then(
				() => formVerified(newPost), //no issues with the data provided
				() => alert("Image URL is not valid.") //
			);
	});

  //Validates if the provided link contains image
	function doesImageLoad(url)
	{
		const img = new Image();
		img.src = url;

		return new Promise((resolve, reject) =>
		{
			img.onload = () => resolve();
			img.onerror = () => reject();
		});
	}

  /**
   * Adds new post information to localStorage,
   * refreshes display and year filter below to include the new post,
   * resets the submition form
  */
	function formVerified(newPost)
	{
		let posts = JSON.parse(localStorage.getItem("posts"));
		posts.push(newPost);
		localStorage.setItem("posts", JSON.stringify(posts));

		createPostDisplay();
		dropDownList = fillFilter();
		resetForm(createPostForm);
	}

	function resetForm(form)
	{
		form.reset();
		document.getElementById("datePicker").valueAsDate = new Date(); //current date as default value
	}

  /**
   * Creates a list of blog post filtered by given year.
   * Displays the information in seperated boxes.
  */
	function createPostDisplay()
	{
		let container = document.querySelector("#postsContainer");
		let posts = JSON.parse(localStorage.getItem("posts"));
		if(posts != null)
		{
			container.replaceChildren();

			posts.forEach(post =>
			{
				let dateElement = document.createElement("p");
				let dateNode = document.createTextNode(post.date);
				dateElement.appendChild(dateNode);
				let year = (new Date(post.date)).getFullYear();
				if(getSelectedYear() == year)
				{
					let card = document.createElement("div");
					card.setAttribute("id", "postDisplay");

					card.appendChild(dateElement);

					let nameElement = document.createElement("h2");
					let nameNode = document.createTextNode(post.name);
					nameElement.appendChild(nameNode);
					card.appendChild(nameElement);

					let pictureElement = document.createElement("img");
					pictureElement.setAttribute("src", post.url);
					card.appendChild(pictureElement);
                    
					let commentElement = document.createElement("p");
					commentElement.appendChild(document.createTextNode(post.comment));
					let commentBox = document.createElement("div");
					commentBox.setAttribute("id", "commentBox");
					commentBox.appendChild(commentElement);

					card.appendChild(commentBox);

					container.appendChild(card);
				}
			});
		}
	}

  //Fills the drop-down list with 2022 and years that has at least one post
	function fillFilter()
	{
		let filterElement = document.getElementById("filter");
		let posts = JSON.parse(localStorage.getItem("posts"));

		if(posts != null)
			posts.forEach(post =>
			{
				let yearOption = document.createElement("option");
				let year = (new Date(post.date)).getFullYear();
				if(yearsList.includes(year) == false) //create a value in the filter only if it does not exist in yearsList
				{
					yearsList.push(year);
					let yearNode = document.createTextNode(year);
					yearOption.appendChild(yearNode);
					filterElement.appendChild(yearOption);
				}
			});

		return filterElement;
	}

  //Returns value of the year that is selected in the drop-down filter
	function getSelectedYear()
	{
		let dropDownList = document.getElementById("filter");
		return dropDownList.options[dropDownList.selectedIndex].value;
	}
};